import pdftotext

# Load your PDF
fname='simple_memo.pdf'
with open(fname, "rb") as f:
    pdf = pdftotext.PDF(f)

# If it's password-protected
#with open("secure.pdf", "rb") as f:
#    pdf = pdftotext.PDF(f, "secret")

# How many pages?
print(len(pdf))

# Iterate over all the pages
#for page in pdf:
#    print(page)

# Read some individual pages
#print(pdf[0])


for i in pdf:
    print(i)

#print(page.split())

for page in pdf:
    for line in page.split():
        print(line)

#print(pdf[1])

# Read all the text into one string
#print("\n\n".join(pdf))
