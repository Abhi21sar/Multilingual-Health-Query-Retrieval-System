def get_feedback(tree):

    # feedback = driver.find_element("xpath","//div[@id='user_feedback']//div[@class='DrugPane__content___3-yrB']/div[@class='style__container___H5Qpz']")
    # feedback_rows = feedback.find_elements("xpath",".//div[@class='row']")

    feedback = tree.xpath("//div[@id='user_feedback']//div[@class='DrugPane__content___3-yrB']/div[@class='style__container___H5Qpz']")[0]

    feedback_rows = feedback.xpath(".//div[@class='row']")

    feedback_dict = {}

    for row in feedback_rows:

        # cols = row.find_elements("xpath",".//div[@class='style__container___1nARz']")
        cols = row.xpath(".//div[@class='style__container___1nARz']")

        for col in cols:

            # q = col.find_element("xpath",'./span')
            # print(q.text)
            q = col.xpath('./span/text()')[0]

            # responses = col.find_elements("xpath",".//div[@class='style__container___3DWmB']")
            responses = col.xpath(".//div[@class='style__container___3DWmB']")
            responses_list = []

            for response in responses:

                # r = response.find_element("xpath",".//div[@class='style__details-text___3mMMv']")
                # print(r.text)
                r = response.xpath(".//div[@class='style__details-text___3mMMv']/text()")[0]

                # percent = response.find_element("xpath",".//div[@class='style__percentage___1FkC_']")
                # print(percent.text)
                percent = response.xpath(".//div[@class='style__percentage___1FkC_']/text()")[0]

                # responses_list.append((r.text,percent.text))
                responses_list.append((r,percent))

            # feedback_dict[q.text] = responses_list
            feedback_dict[q] = responses_list

    return feedback_dict


def get_faq(tree):

    # faq = driver.find_element("xpath","//div[@id='faq']//div[@class='Faqs__tile___1B58W']")
    faq = tree.xpath("//div[@id='faq']//div[@class='Faqs__tile___1B58W']")

    # faq_dict = {}
    faq_list = []

    # FAQs seen on the page

    # faq_direct = faq.find_elements("xpath","./div")[0:4]
    faq_direct = faq[0].xpath("./div")[0:4]

    # faq_hidden = faq.find_elements("xpath","./div[@class='Faqs__content___2_NYj']/div")
    faq_hidden = faq[0].xpath("./div[@class='Faqs__content___2_NYj']/div")

    for f in faq_direct:

        # q = f.find_element("xpath","./h3").text[3:]
        q = f.xpath("./h3/text()")[0][3:]

        # a = f.find_element("xpath","./div").text
        a = f.xpath("./div/text()")[0]

        # faq_dict[q] = a
        faq_list.append((q,a))

    for f in faq_hidden:

        # q = f.find_element("xpath","./h3").text[3:]
        q = f.xpath("./h3/text()")[0][3:]

        # a = f.find_element("xpath","./div").text
        a = f.xpath("./div/text()")[0]

        # faq_dict[q] = a
        faq_list.append((q,a))

    return faq_list

def get_patient_concerns(tree):

    # tree = html.fromstring(driver.page_source)
    patient_concerns = tree.xpath("//div[@id='patient_concerns']/div[@class='DrugPane__content___3-yrB']//div[@class='slick-track']/div[contains(@class,'slick-slide')]/div/div/div")

    # patient_concerns_dict = {}
    patient_concerns_list = []

    for ele in patient_concerns:

        q = ele.xpath("./div[contains(@class,'style__question___')]/text()")[0]
        a = ele.xpath("./div[contains(@class,'style__answer___')]/text()")[0]

        # patient_concerns_dict[q] = a
        patient_concerns_list.append((q,a))

    return patient_concerns_list


def get_side_effects(tree):

    side_effects = tree.xpath("//div[@id='side_effects']//div[@class='DrugOverview__content___22ZBX']/div")[0]

    # side_effects_dict = {}
    side_effects_list = []

    # side_effects_dict['Side Effects'] = side_effects.xpath('.//text()')
    side_effects_list = side_effects.xpath('.//text()')

    return side_effects_list
