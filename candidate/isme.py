from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfdoc
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from django.conf import settings
from PIL import Image

# Import our font
registerFont(TTFont('Inconsolata', ''.join(settings.STATICFILES_DIRS) + '/fonts/Calibri_Regular.TTF'))
registerFont(TTFont('InconsolataBold', ''.join(settings.STATICFILES_DIRS) + '/fonts/Calibri Bold.TTF'))
registerFontFamily('Inconsolata', normal='Inconsolata', bold='InconsolataBold')


def generate_print_pdf(data, edu, resume_detalis):
    # Set the page height and width
    HEIGHT = 11 * inch
    WIDTH = 8.5 * inch

    # Set our styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Content',
                              fontFamily='Inconsolata',
                              fontSize=10,
                              spaceAfter=0.001 * inch,
                              bulletFontSize=15
                              ))

    styles.add(ParagraphStyle(name='Date',
                              fontFamily='Inconsolata',
                              fontSize=10,
                              spaceAfter=0.001 * inch,
                              alignment=TA_RIGHT))

    styles.add(ParagraphStyle(name='Heading',
                              fontFamily='InconsolataBold',
                              fontSize=10,
                              spaceAfter=.5 * inch,
                              alignment=TA_LEFT,
                              backColor=(0.866, 0.898, 0.929),
                              borderPadding=1.6))

    styles.add(ParagraphStyle(name='JobRole',
                              fontFamily='Inconsolata',
                              fontSize=10,
                              spaceAfter=.001 * inch,
                              alignment=TA_CENTER, ))

    descStyle = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        # ('BOX', (0,0), (-1,-1), 0.25, colors.black)
    ])

    headingStyle = TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
        # ('BOX', (0,0), (-1,-1), 0.25, colors.black)
    ])

    pdfname = 'media/temp/create_resume/{}.pdf'.format(resume_detalis["name"])
    doc = SimpleDocTemplate(
        pdfname,
        pagesize=letter,
        bottomMargin=.05 * inch,
        topMargin=1 * inch,
        rightMargin=0.15 * inch,
        leftMargin=0.15 * inch)  # set the doc template
    style = styles["Normal"]  # set the style to normal
    story = []  # create a blank story to tell

    # table for displaying right part of the resume
    contentTable = Table(
        data,
        colWidths=[7.7 * inch])
    contentStyle = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONT', (0, 0), (-1, -1), 'Inconsolata'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('LEFTPADDING',(0,0),(-1,-1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        # ('RIGHTPADDING',(0,0),(-1,-1), 0),
        # ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        # ('BOX', (0,0), (-1,-1), 0.25, colors.black)
    ])
    contentTable.setStyle(contentStyle)

    # table for showing top part of the resume ie education details.
    eduTable = Table(
        edu,
        # the sum of all column widths should be 7.8 inch (widht of the page) for end to end.
        colWidths=[1.9 * inch, 2.1 * inch, 2.1 * inch, 0.6 * inch, 0.8 * inch],
    )
    eduStyle = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONT', (0, 0), (-1, 0), 'InconsolataBold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, 0), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONT', (0, 1), (-1, -1), 'Inconsolata'),
    ])
    eduTable.setStyle(eduStyle)

    education_tag = Table(
        [[Paragraph('<b>Academic Qualification</b>', styles['Heading'])]],
        colWidths=[7.5 * inch],
    )
    education_tag.setStyle(headingStyle)

    # appending the changes to the story
    story.append(education_tag)
    story.append(Spacer(inch, 0.1 * inch))
    story.append(eduTable)
    story.append(Spacer(inch, 0.1 * inch))
    story.append(contentTable)
    doc.build(story, onFirstPage=myPageWrapper(resume_detalis))


"""
    Draw the framework for the first page,
    pass in contact info as a dictionary
"""


def myPageWrapper(data):
    # template for static, non-flowables, on the first page
    # draws all of the contact information at the top of the page
    # Set the page height and width
    HEIGHT = 11 * inch
    WIDTH = 8.5 * inch

    def myPage(canvas, doc):
        canvas.saveState()  # save the current state
        # set the font for the name
        # canvas.line(0.35*inch, HEIGHT - (1.4*inch), WIDTH - (0.35*inch), HEIGHT - (1.4*inch))
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont('InconsolataBold', 12)
        canvas.drawString(0.6 * inch, HEIGHT - (0.5 * inch), data["name"])
        canvas.setFont('Inconsolata', 10)
        canvas.drawString(0.6 * inch, HEIGHT - (0.7 * inch), "ID Number: " + data["Roll_No"])
        canvas.drawString(0.6 * inch, HEIGHT - (0.9 * inch), data["gender"] + " | " + data["DOB"].strftime('%d/%m/%Y'))
        # for school image
        # im = Image.open("logo1.jpg")
        # canvas.drawInlineImage(im, .4*inch,HEIGHT - (1.3 * inch), width=65, height=65)
        # for profile image
        # im = Image.open("photo.jpg")
        # canvas.drawInlineImage(im, 6.25*inch,HEIGHT - (1.3 * inch), width=55, height=55)
        # for qrcode
        # for school name
        # canvas.setFont('Inconsolata', 9)
        # canvas.drawCentredString( 4.25*inch,.5*inch ,"Indian School of Management and Entrepreneurship, Mumbai")
        # for company name
        # canvas.drawCentredString(4.25*inch,.37* inch,": 022-42355678/77 | : Info@isme.in")
        # for drawing the page border
        # canvas.rect(0.1*inch,0.1*inch,8.3*inch,10.8*inch)
        # restore the state to what it was when save
        canvas.setFont('Inconsolata', 10)
        canvas.drawCentredString(4 * inch, .3 * inch, "Powered by")
        canvas.setFont('InconsolataBold', 10)
        canvas.drawCentredString(4.55 * inch, .3 * inch, " apli.ai")
        canvas.restoreState()

    return myPage


def generate_pdf(resume_detalis):
    # general details
    profile_name = resume_detalis["name"]
    main_content = {
        'Professional Experience': resume_detalis['Professional Experience'],
        'Academic / Industrial Projects': resume_detalis['Academic / Industrial Projects'],
        'Extracurricular Activities': resume_detalis['Extracurricular Activities'],
        'Skills': resume_detalis['Skills'],
        'Awards and Certifications': resume_detalis['Awards']
    }
    tblData = []

    # Set our styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Content',
                              fontFamily='Inconsolata',
                              fontSize=10,
                              spaceAfter=0.001 * inch,
                              bulletFontSize=15
                              ))

    styles.add(ParagraphStyle(name='Date',
                              fontFamily='Inconsolata',
                              fontSize=10,
                              spaceAfter=0.001 * inch,
                              alignment=TA_RIGHT))

    styles.add(ParagraphStyle(name='Heading',
                              fontFamily='InconsolataBold',
                              fontSize=10,
                              spaceAfter=.5 * inch,
                              alignment=TA_LEFT,
                              backColor=(0.866, 0.898, 0.929),
                              borderPadding=1.6))

    styles.add(ParagraphStyle(name='JobRole',
                              fontFamily='Inconsolata',
                              fontSize=10,
                              spaceAfter=.001 * inch,
                              alignment=TA_CENTER, ))

    descStyle = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        # ('BOX', (0,0), (-1,-1), 0.25, colors.black)
    ])

    headingStyle = TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
        # ('BOX', (0,0), (-1,-1), 0.25, colors.black)
    ])

    # for appending the resume details
    for par in main_content.keys():
        if main_content[par] is not None:
            tab1 = Table([[Paragraph('<b>{}</b>'.format(par), styles['Heading'])]])
            tab1.setStyle(headingStyle)
            tblData.append([tab1])
            for content in main_content[par]:
                if par == 'Professional Experience':
                    tab = Table([[Paragraph('{}'.format(content[0]), styles['Content']),
                                  Paragraph('{}'.format(content[1]), styles['JobRole']),
                                  Paragraph('{}'.format(content[2]), styles['Date'])]],
                                colWidths=[2.2 * inch, 4.1 * inch, 1.2 * inch])
                    tab.setStyle(descStyle)
                    tblData.append([tab])
                    tblData.append([[Paragraph(x, styles['Content'], bulletText=u'\u2022') for x in content[3:]]])
                elif par == 'Academic / Industrial Projects' or par == 'Extracurricular Activities':
                    tab = Table([[Paragraph('{}'.format(content[0]), styles['Content']),
                                  Paragraph('{}'.format(content[1]), styles['Date'])]],
                                colWidths=[6.1 * inch, 1.4 * inch])
                    tab.setStyle(descStyle)
                    tblData.append([tab])
                    tblData.append([[Paragraph(x, styles['Content'], bulletText=u'\u2022') for x in content[2:]]])
                elif par == 'Skills':
                    for eachval in content:
                        tab = Table([[Paragraph('{}'.format(eachval), styles['Content'], bulletText=u'\u2022')]])
                        tab.setStyle(descStyle)
                        tblData.append([tab])
                else:
                    tab = Table([[Paragraph('{}'.format(content[0]), styles['Content'], bulletText=u'\u2022'),
                                  Paragraph('{}'.format(content[1]), styles['Date'])]],
                                colWidths=[6.1 * inch, 1.4 * inch])
                    tab.setStyle(descStyle)
                    tblData.append([tab])

    try:
        generate_print_pdf(tblData, resume_detalis['Academic Qualification'], resume_detalis)
    except (ValueError, KeyError, AttributeError) as e:
        print(e)
