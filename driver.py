from using_url_wiki import url_driver
from using_doc import doc_driver
from using_pdf import pdf_driver
from using_social import social_driver
print("Select the input source type: ")
print("1. URL or Wikipedia")
print("2. Text document")
print("3. PDF")
print("4. Social media and RSS feeds")
n = int(input("Enter your choice: "))
if(n==1):
	url_driver()
elif(n==2):
	doc_driver()
elif(n==3):
	pdf_driver()
elif(n==4):
	social_driver()

