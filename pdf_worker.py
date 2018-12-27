import fpdf
from time import gmtime, strftime


def create_payment_document(data):
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    # pdf.set_font("Arial", size=15)
    pdf.cell(50, 15, 'INN', 0, 0, 'L')
    pdf.cell(65, 15, data['name'], 0, 1, 'L')
    pdf.cell(50, 15, 'BIK', 0, 0, 'L')
    pdf.cell(65, 15, data['bik'], 0, 1, 'L')
    pdf.cell(50, 15, 'Account number', 0, 0, 'L')
    pdf.cell(65, 15, data['numAccount'], 0, 1, 'L')
    pdf.cell(50, 15, 'NDS', 0, 0, 'L')
    pdf.cell(65, 15, data['nds'], 0, 1, 'L')
    pdf.cell(50, 15, 'Amount', 0, 0, 'L')
    pdf.cell(65, 15, data['amount'], 0, 1, 'L')
    datestamp = strftime("%a %d %b %Y %H:%M:%S", gmtime())
    pdf.cell(65, 15, "Date of creation - " + datestamp, 0, 1, 'L')
    name = "payment_"+ datestamp.replace(' ','_') + ".pdf"
    pdf.output(name)

    return name
# create_payment_document({
#     'inn':'1234567890',
#     'bik':'123456789',
#     'num_account': '12345678900987654321',
#     'nds': '18%',
#     'amount': '1500'
# })