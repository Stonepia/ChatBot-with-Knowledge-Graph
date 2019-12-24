from query import Query
import re

class QuestionTemplate():
    def __init__(self):
        self.q_template_dict={
            0: self.get_company_birthday,#0:self.get_movie_rating,    #13:self.get_actor_birthday
            1: self.get_company_introduction, #3:self.get_movie_introduction,经营范围
            2: self.get_company_type, #2:self.get_movie_type,
            3: self.get_company_registerCap, # 12:self.get_actor_movie_num, 资金
            8: self.get_company_registerCap_bigger, #8:self.get_movie_rating_bigger,
            9: self.get_company_registerCap_smaller#9:self.get_movie_rating_smaller,
        }

        # 连接数据库
        self.graph = Query()
        # 测试数据库是否连接上
        # result=self.graph.run("match (m:Movie)-[]->() where m.title='卧虎藏龙' return m.rating")
        # print(result)
        # exit()

    def get_question_answer(self,question,template):
        # 如果问题模板的格式不正确则结束
        assert len(str(template).strip().split("\t"))==2
        template_id,template_str=int(str(template).strip().split("\t")[0]),str(template).strip().split("\t")[1]
        self.template_id=template_id
        self.template_str2list=str(template_str).split()

        # 预处理问题
        question_word,question_flag=[],[]
        for one in question:
            word, flag = one.split("/")
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag)==len(question_word)
        self.question_word=question_word
        self.question_flag=question_flag
        self.raw_question=question
        # 根据问题模板来做对应的处理，获取答案
        answer=self.q_template_dict[template_id]()
        return answer

    # 获取电影名字
    def get_company_name(self):  #get_movie_name 111
        ## 获取nm在原问题中的下标
        tag_index = self.question_flag.index("nm")
        ## 获取电影名称
        company_name = self.question_word[tag_index]  #movie_name = self.question_word[tag_index] 111
        return company_name#return movie_name
    def get_name(self,type_str):
        name_count=self.question_flag.count(type_str)
        if name_count==1:
            ## 获取nm在原问题中的下标
            tag_index = self.question_flag.index(type_str)
            ## 获取电影名称
            name = self.question_word[tag_index]
            return name
        else:
            result_list=[]
            for i,flag in enumerate(self.question_flag):
                if flag==str(type_str):
                    result_list.append(self.question_word[i])
            return result_list

    def get_num_x(self):
        x = re.sub(r'\D', "", "".join(self.question_word))
        return x
    # 0:nm 成立日期
    def get_company_birthday(self):
        company_name = self.get_company_name()
        cql = f"match (m:Stock)-[]->() where m.name='{company_name}' return m.setupDate" #111
        print(cql)
        answer = self.graph.run(cql)[0]
        print(answer)
        answer = round(answer, 2)
        final_answer=company_name+"成立日期为"+str(answer)
        return final_answer
    # 1:nm 经营范围√
    def get_company_introduction(self):
        company_name = self.get_company_name()
        cql = f"match(m:Stock)-[]->() where m.name='{company_name}' return m.businessScope"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = company_name + "经营范围为：" + str(answer) + "！"
        return final_answer
    # 2:nm 行业√
    def get_company_type(self):
        company_name = self.get_company_name()
        cql =f"match(m:Stock)-[r:is_industry_of]->(b) where m.name='{company_name}' return b.name"
            #"match(m:Stock)-[r:industry_of]->(b) where m.name='{company_name}' return b.name"
            #match(m:Company)-[r:industry_of]->(b) where m.name="东材科技" return b.name
            #f"MATCH (:Stock{name:“东财科技”}) -- (industry:Industry) RETURN industry.name"
            #f"match(m:Stock)-[r:is]->(industry：Industry) where m.name='{company_name}' return industry.name"
        print(cql)
        answer = self.graph.run(cql)
        answer_set=set(answer)
        answer_list=list(answer_set)
        answer="、".join(answer_list)
        final_answer = company_name + "属于" + str(answer) + "！"
        return final_answer
    # 3:nm 注册资本√
    def get_company_registerCap(self):
        company_name = self.get_company_name()
        cql = f"match(m:Stock)-[]->() where m.name='{company_name}' return m.registerCap"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = company_name + "注册资本为：" + str(answer) + "！"
        return final_answer
    # 8:注册资本 大于 x
    def get_company_registerCap_bigger(self):
        x=self.get_num_x()
        cql = f"match(m:Stock)-[]->() where m.registerCap>={x} return m.name"
        print(cql)
        answer = self.graph.run(cql)
        answer = "、".join(answer)
        answer = str(answer).strip()
        final_answer = "公司注册资本大于"+x+"万的有"+answer+"等！"
        return final_answer
    #9:
    def get_company_registerCap_smaller(self):
        x = self.get_num_x()
        cql = f"match(m:Stock)-[]->() where m.registerCap<{x} return m.name"
        print(cql)
        answer = self.graph.run(cql)
        answer = "、".join(answer)
        answer = str(answer).strip()
        final_answer = "公司注册资本小于" + x + "万的有" + answer + "等！"
        return final_answer
