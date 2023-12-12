from lxml import etree
from io import StringIO
import json


class Splitter:
    def __init__(self):
        html = open("index.html", "r").read()
        parser = etree.HTMLParser()
        self.tree = etree.parse(StringIO(html), parser)
        # result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
        self.split_html()

    def split_html(self):
        result = []
        parse = self.tree
        for head in parse.xpath("//h1/a"):
            title = head.text
            section = ""
            html = etree.tostring(head).decode()
            result.append(
                {
                    "title": title,
                    "section": section,
                    "html": html
                }
            )
        for sec in parse.xpath("//section/h2/a/span[@class='section-number']"):
            title,section,html = self.parseSection(sec)
            result.append(
                {
                    "title": title,
                    "section": section,
                    "html": html
                }
            )
        
        # export result to json
        ljson = json.dumps(result)
        a=open("result.json", "w")
        a.write(ljson)
        a.close()

        return result
    
    def parseSection(self, html: str):
        title = html.getparent().getparent().find("a/span[@class='section-title']").text
        section = html.getparent().find("span[@class='section-number']").text
        html = etree.tostring(html.getparent().getparent().getparent()).decode()
        return title,section,html

if __name__=="__main__":
    Splitter()
