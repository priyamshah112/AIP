from django.core.mail import send_mail
from string import ascii_lowercase,ascii_uppercase
import string

def selmail(ssubject,smessage,r,cname,cpost):
    subject=ssubject
    scname=cname
    scpost=cpost
    message=""
    message1=smessage
    print(subject,scname,scpost,message,message1)
    html_message1="""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<!--[if !mso]><!-->
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<!--<![endif]-->
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title></title>
<style type="text/css">
* {{-webkit-font-smoothing: antialiased;}}
body {{
    Margin: 0;
    padding: 0;
    min-width: 100%;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    mso-line-height-rule: exactly;
}}
table {{
    border-spacing: 0;
    color: #333333;
    font-family: Arial, sans-serif;
}}
img{{
    border: 0;
}}
.wrapper {{
    width: 100%;
    table-layout: fixed;
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
}}
.webkit {{
    max-width: 600px;
}}
.outer {{
    Margin: 0 auto;
    width: 100%;
    max-width: 600px;
}}
.full-width-image img {{
    width: 100%;
    max-width: 600px;
    height: auto;
}}
.inner {{
    padding: 10px;
}}
p {{
    Margin: 0;
    padding-bottom: 10px;
}}
.h1 {{
    font-size: 21px;
    font-weight: bold;
    Margin-top: 15px;
    Margin-bottom: 5px;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.h2 {{
    font-size: 18px;
    font-weight: bold;
    Margin-top: 10px;
    Margin-bottom: 5px;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.one-column .contents {{
    text-align: left;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.one-column p {{
    font-size: 14px;
    Margin-bottom: 10px;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.two-column {{
    text-align: center;
    font-size: 0;
}}
.two-column .column {{
    width: 100%;
    max-width: 300px;
    display: inline-block;
    vertical-align: top;
}}
.contents {{
    width: 100%;
}}
.two-column .contents {{
    font-size: 14px;
    text-align: left;
}}
.two-column img {{
    width: 100%;
    max-width: 280px;
    height: auto;
}}
.two-column .text {{
    padding-top: 10px;
}}
.three-column {{
    text-align: center;
    font-size: 0;
    padding-top: 10px;
    padding-bottom: 10px;
}}
.three-column .column {{
    width: 100%;
    max-width: 200px;
    display: inline-block;
    vertical-align: top;
}}
.three-column .contents {{
    font-size: 14px;
    text-align: center;
}}
.three-column img {{
    width: 100%;
    max-width: 180px;
    height: auto;
}}
.three-column .text {{
    padding-top: 10px;
}}
.img-align-vertical img {{
    display: inline-block;
    vertical-align: middle;
}}
@media only screen and (max-device-width: 480px) {{
table[class=hide], img[class=hide], td[class=hide] {{
    display: none !important;
}}
.contents1 {{
    width: 100%;
}}
.contents1 {{
    width: 100%;
}}
.center {{
  display: block;
  margin-left: auto;
  right: 30px;
  height: 20px
  width: 20px;
}}
</style>
</head>

<body style="Margin:0;padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;min-width:100%;background-color:#f3f2f0;">
<center class="wrapper" style="width:100%;table-layout:fixed;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;background-color:#f3f2f0;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f3f2f0;" bgcolor="#f3f2f0;">
    <tr>
      <td width="100%"><div class="webkit" style="max-width:600px;Margin:0 auto;">
          
          <!-- ======= start main body ======= -->
          <table class="outer" align="center" cellpadding="0" cellspacing="0" border="0" style="border-spacing:0;Margin:0 auto;width:100%;max-width:600px;">
            <tr>
              <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;"><!-- ======= start header ======= -->
                
                <table border="0" width="100%" cellpadding="0" cellspacing="0"  >
                  <tr>
                    <td><table style="width:100%;" cellpadding="0" cellspacing="0" border="0">
                        <tbody>
                          <tr>
                            <td align="center"><center>
                                <table border="0" align="center" width="100%" cellpadding="0" cellspacing="0" style="Margin: 0 auto;">
                                  <tbody>
                                    <tr>
                                      <td class="one-column" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" bgcolor="#FFFFFF"><!-- ======= start header ======= -->
                                        
                                        <table cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="#f3f2f0">
                                          <tr>
                                            <td class="two-column" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;text-align:left;font-size:0;" >
                                              <div class="column" style="width:100%;max-width:80px;display:inline-block;vertical-align:top;">
                                                <table class="contents" style="border-spacing:0; width:100%"  >
                                                  <tr>
                                                    <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:5px;" align="left"><a href="#" target="_blank"><img src="#" alt="" width="60" height="60" style="border-width:0; max-width:60px;height:auto; display:block" align="left"/></a></td>
                                                  </tr>
                                                </table>
                                              </div>
                                              <div class="column" style="width:100%;max-width:518px;display:inline-block;vertical-align:top;">
                                                <table width="100%" style="border-spacing:0" cellpadding="0" cellspacing="0" border="0" >
                                                  <tr>
                                                    <td class="inner" style="padding-top:0px;padding-bottom:10px; padding-right:10px;padding-left:10px;"><table class="contents" style="border-spacing:0; width:100%" cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                          <td align="left" valign="top">&nbsp;</td>
                                                        </tr>
                                                      </table></td>
                                                  </tr>
                                                </table>
                                              </div>
                                            </td>
                                          </tr>
                                          <tr>
                                            <td>&nbsp;</td>
                                          </tr>
                                        </table></td>
                                    </tr>
                                  </tbody>
                                </table>
                              </center></td>
                          </tr>
                        </tbody>
                      </table></td>
                  </tr>
                </table>
                
                <!-- ======= end header ======= --> 
                
                <!-- ======= start hero image ======= --><!-- ======= end hero image ======= --> 
                
                <!-- ======= start hero article ======= -->
                
                <table class="one-column" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0; border-left:1px solid #e8e7e5; border-right:1px solid #e8e7e5; border-bottom:1px solid #e8e7e5; border-top:1px solid #e8e7e5" bgcolor="#FFFFFF">
                  <tr>
                    <td align="left" style="padding:50px 50px 50px 50px"><p style="color:#262626; font-size:24px; text-align:left; font-family: Verdana, Geneva, sans-serif"><strong>Congratulations!!!&emsp;</strong><img src="https://images.vexels.com/media/users/3/134595/isolated/preview/525928028c88f02fb50261dd70ceb749-happy-emoticon-emoji-by-vexels.png" alt="successful" class="center" align="middle" height=65 width=65 style="top: 40px"></p>
                      <p style="color:#000000; font-size:16px; text-align:left; font-family: Verdana, Geneva, sans-serif; line-height:22px "><b>Dear {},</b><br>{}<br />
                        <br />
                        <br />
                      </p>
                      <table border="0" align="left" cellpadding="0" cellspacing="0" style="Margin:0 auto;">
                        <tbody>
                          <tr>
                            <td align="center"><table border="0" cellpadding="0" cellspacing="0" style="Margin:0 auto;">
                                <tr>
                                  <td width="250" height="60" align="center" bgcolor="#752873" style="-moz-border-radius: 30px; -webkit-border-radius: 30px; border-radius: 30px;"><a href="http://127.0.0.1:8000/accounts/login"  style="width:250; display:block; text-decoration:none; border:0; text-align:center; font-weight:bold;font-size:18px; font-family: Arial, sans-serif; color: #ffffff" class="button_link">Log In<img src="https://gallery.mailchimp.com/fdcaf86ecc5056741eb5cbc18/images/ac08f159-2260-46e0-a7f0-d196c81eb6cc.jpg" width="32" height="17" style="padding-top:5px" alt="" border="0"/></a></td>
                                </tr>
                              </table></td>
                          </tr>
                        </tbody>
                      </table>
                      <p style="color:#000000; font-size:16px; text-align:left; font-family: Verdana, Geneva, sans-serif; line-height:22px "><br />
                        <br />
                        <br />
                        <br />
                        <br />
                        Best Regards, <br />
                        <a href="#" target="_blank"><img src="#" alt="" width="60" height="60" style="border-width:0; max-width:60px;height:auto; display:block" align="left"/></a>Team AMP Tech</p></td>
                  </tr>
                </table>
                
                <!-- ======= end hero article ======= --> 
                
                <!-- ======= start footer ======= -->
                
                <table cellpadding="0" cellspacing="0" border="0" width="100%">
                  <tr>
                    <td height="30">&nbsp;</td>
                  </tr>
                  <tr>
                    <td class="two-column" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;text-align:center;font-size:0;">
                      <div class="column" style="width:100%;max-width:350px;display:inline-block;vertical-align:top;">
                        <table class="contents" style="border-spacing:0; width:100%">
                          <tr>

                            <td width="61%" align="left" valign="middle" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;"><p style="color:#787777; font-size:13px; text-align:left; font-family: Verdana, Geneva, sans-serif"> AMP Tech &copy; 2020<br />
                                </p></td>
                          </tr>
                        </table>
                      </div>
 
                      <div class="column" style="width:100%;max-width:248px;display:inline-block;vertical-align:top;">
                        <table width="100%" style="border-spacing:0">
                          <tr>
                            <td class="inner" style="padding-top:0px;padding-bottom:10px; padding-right:10px;padding-left:10px;"><table class="contents" style="border-spacing:0; width:100%">
                                <tr>
                                  <td width="32%" align="center" valign="top" style="padding-top:10px"><table width="150" border="0" cellspacing="0" cellpadding="0">
                                    <tr>

                                    </tr>
                                  </table></td>
                                </tr>
                              </table></td>
                          </tr>
                        </table>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td height="30">&nbsp;</td>
                  </tr>
                </table>
                <!-- ======= end footer ======= --></td>
            </tr>
          </table>
        </div></td>
    </tr>
  </table>
</center>
</body>
</html>
"""
    html_message=html_message1.format(scname,message1)
    recipient_list = [r,]
    print(recipient_list)
    send_mail(subject, message,'mum.amptech@gmail.com', recipient_list,html_message=html_message,fail_silently=False,)
    print("mail sent hired")

def rejmail(rsubject,rmessage,r,cname,cpost):
    subject=rsubject
    rcname=cname
    rcpost=cpost
    message1=rmessage
    message=""
    html_message1="""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<!--[if !mso]><!-->
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<!--<![endif]-->
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title></title>
<style type="text/css">
* {{-webkit-font-smoothing: antialiased;}}
body {{
    Margin: 0;
    padding: 0;
    min-width: 100%;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    mso-line-height-rule: exactly;
}}
table {{
    border-spacing: 0;
    color: #333333;
    font-family: Arial, sans-serif;
}}
img{{
    border: 0;
}}
.wrapper {{
    width: 100%;
    table-layout: fixed;
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
}}
.webkit {{
    max-width: 600px;
}}
.outer {{
    Margin: 0 auto;
    width: 100%;
    max-width: 600px;
}}
.full-width-image img {{
    width: 100%;
    max-width: 600px;
    height: auto;
}}
.inner {{
    padding: 10px;
}}
p {{
    Margin: 0;
    padding-bottom: 10px;
}}
.h1 {{
    font-size: 21px;
    font-weight: bold;
    Margin-top: 15px;
    Margin-bottom: 5px;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.h2 {{
    font-size: 18px;
    font-weight: bold;
    Margin-top: 10px;
    Margin-bottom: 5px;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.one-column .contents {{
    text-align: left;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.one-column p {{
    font-size: 14px;
    Margin-bottom: 10px;
    font-family: Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.two-column {{
    text-align: center;
    font-size: 0;
}}
.two-column .column {{
    width: 100%;
    max-width: 300px;
    display: inline-block;
    vertical-align: top;
}}
.contents {{
    width: 100%;
}}
.two-column .contents {{
    font-size: 14px;
    text-align: left;
}}
.two-column img {{
    width: 100%;
    max-width: 280px;
    height: auto;
}}
.two-column .text {{
    padding-top: 10px;
}}
.three-column {{
    text-align: center;
    font-size: 0;
    padding-top: 10px;
    padding-bottom: 10px;
}}
.three-column .column {{
    width: 100%;
    max-width: 200px;
    display: inline-block;
    vertical-align: top;
}}
.three-column .contents {{
    font-size: 14px;
    text-align: center;
}}
.three-column img {{
    width: 100%;
    max-width: 180px;
    height: auto;
}}
.three-column .text {{
    padding-top: 10px;
}}
.img-align-vertical img {{
    display: inline-block;
    vertical-align: middle;
}}
@media only screen and (max-device-width: 480px) {{
table[class=hide], img[class=hide], td[class=hide] {{
    display: none !important;
}}
.contents1 {{
    width: 100%;
}}
.contents1 {{
    width: 100%;
}}
.center {{
  display: block;
  margin-left: auto;
  right: 30px;
  height: 20px
  width: 20px;
}}
</style>
</head>

<body style="Margin:0;padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;min-width:100%;background-color:#f3f2f0;">
<center class="wrapper" style="width:100%;table-layout:fixed;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;background-color:#f3f2f0;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f3f2f0;" bgcolor="#f3f2f0;">
    <tr>
      <td width="100%"><div class="webkit" style="max-width:600px;Margin:0 auto;">
          
          <!-- ======= start main body ======= -->
          <table class="outer" align="center" cellpadding="0" cellspacing="0" border="0" style="border-spacing:0;Margin:0 auto;width:100%;max-width:600px;">
            <tr>
              <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;"><!-- ======= start header ======= -->
                
                <table border="0" width="100%" cellpadding="0" cellspacing="0"  >
                  <tr>
                    <td><table style="width:100%;" cellpadding="0" cellspacing="0" border="0">
                        <tbody>
                          <tr>
                            <td align="center"><center>
                                <table border="0" align="center" width="100%" cellpadding="0" cellspacing="0" style="Margin: 0 auto;">
                                  <tbody>
                                    <tr>
                                      <td class="one-column" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" bgcolor="#FFFFFF"><!-- ======= start header ======= -->
                                        
                                        <table cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="#f3f2f0">
                                          <tr>
                                            <td class="two-column" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;text-align:left;font-size:0;" >
                                              <div class="column" style="width:100%;max-width:80px;display:inline-block;vertical-align:top;">
                                                <table class="contents" style="border-spacing:0; width:100%"  >
                                                  <tr>
                                                    <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:5px;" align="left"><a href="#" target="_blank"><img src="#" alt="" width="60" height="60" style="border-width:0; max-width:60px;height:auto; display:block" align="left"/></a></td>
                                                  </tr>
                                                </table>
                                              </div>
                                              <div class="column" style="width:100%;max-width:518px;display:inline-block;vertical-align:top;">
                                                <table width="100%" style="border-spacing:0" cellpadding="0" cellspacing="0" border="0" >
                                                  <tr>
                                                    <td class="inner" style="padding-top:0px;padding-bottom:10px; padding-right:10px;padding-left:10px;"><table class="contents" style="border-spacing:0; width:100%" cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                          <td align="left" valign="top">&nbsp;</td>
                                                        </tr>
                                                      </table></td>
                                                  </tr>
                                                </table>
                                              </div>
                                            </td>
                                          </tr>
                                          <tr>
                                            <td>&nbsp;</td>
                                          </tr>
                                        </table></td>
                                    </tr>
                                  </tbody>
                                </table>
                              </center></td>
                          </tr>
                        </tbody>
                      </table></td>
                  </tr>
                </table>
                
                <!-- ======= end header ======= --> 
                
                <!-- ======= start hero image ======= --><!-- ======= end hero image ======= --> 
                
                <!-- ======= start hero article ======= -->
                
                <table class="one-column" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0; border-left:1px solid #e8e7e5; border-right:1px solid #e8e7e5; border-bottom:1px solid #e8e7e5; border-top:1px solid #e8e7e5" bgcolor="#FFFFFF">
                  <tr>
                    <td align="left" style="padding:50px 50px 50px 50px"><p style="color:#262626; font-size:24px; text-align:left; font-family: Verdana, Geneva, sans-serif"><strong>Sorry!!!&emsp;</strong><img src="http://pluspng.com/img-png/png-sad-emoji-emoticon-sad-256.png" alt="successful" class="center" align="middle" height=65 width=65 style="top: 40px"></p>
                      <p style="color:#000000; font-size:16px; text-align:left; font-family: Verdana, Geneva, sans-serif; line-height:22px "><b>Dear {},</b><br>{}<br />
                        <br />
                        <br />
                      </p>
                      <table border="0" align="left" cellpadding="0" cellspacing="0" style="Margin:0 auto;">
                        <tbody>
                          <tr>
                            <td align="center"><table border="0" cellpadding="0" cellspacing="0" style="Margin:0 auto;">
                                <tr>
                                  <td width="250" height="60" align="center" bgcolor="#752873" style="-moz-border-radius: 30px; -webkit-border-radius: 30px; border-radius: 30px;"><a href="http://127.0.0.1:8000/accounts/login"  style="width:250; display:block; text-decoration:none; border:0; text-align:center; font-weight:bold;font-size:18px; font-family: Arial, sans-serif; color: #ffffff" class="button_link">Log In<img src="https://gallery.mailchimp.com/fdcaf86ecc5056741eb5cbc18/images/ac08f159-2260-46e0-a7f0-d196c81eb6cc.jpg" width="32" height="17" style="padding-top:5px" alt="" border="0"/></a></td>
                                </tr>
                              </table></td>
                          </tr>
                        </tbody>
                      </table>
                      <p style="color:#000000; font-size:16px; text-align:left; font-family: Verdana, Geneva, sans-serif; line-height:22px "><br />
                        <br />
                        <br />
                        <br />
                        <br />
                        Best Regards, <br />
                        <a href="#" target="_blank"><img src="#" alt="" width="60" height="60" style="border-width:0; max-width:60px;height:auto; display:block" align="left"/></a>Team AMP Tech</p></td>
                  </tr>
                </table>
                
                <!-- ======= end hero article ======= --> 
                
                <!-- ======= start footer ======= -->
                
                <table cellpadding="0" cellspacing="0" border="0" width="100%">
                  <tr>
                    <td height="30">&nbsp;</td>
                  </tr>
                  <tr>
                    <td class="two-column" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;text-align:center;font-size:0;">
                      <div class="column" style="width:100%;max-width:350px;display:inline-block;vertical-align:top;">
                        <table class="contents" style="border-spacing:0; width:100%">
                          <tr>

                            <td width="61%" align="left" valign="middle" style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;"><p style="color:#787777; font-size:13px; text-align:left; font-family: Verdana, Geneva, sans-serif"> AMP Tech &copy; 2020<br />
                                </p></td>
                          </tr>
                        </table>
                      </div>
 
                      <div class="column" style="width:100%;max-width:248px;display:inline-block;vertical-align:top;">
                        <table width="100%" style="border-spacing:0">
                          <tr>
                            <td class="inner" style="padding-top:0px;padding-bottom:10px; padding-right:10px;padding-left:10px;"><table class="contents" style="border-spacing:0; width:100%">
                                <tr>
                                  <td width="32%" align="center" valign="top" style="padding-top:10px"><table width="150" border="0" cellspacing="0" cellpadding="0">
                                    <tr>

                                    </tr>
                                  </table></td>
                                </tr>
                              </table></td>
                          </tr>
                        </table>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td height="30">&nbsp;</td>
                  </tr>
                </table>
                <!-- ======= end footer ======= --></td>
            </tr>
          </table>
        </div></td>
    </tr>
  </table>
</center>
</body>
</html>
"""
    html_message=html_message1.format(rcname,message1)
    recipient_list = [r,]
    send_mail(subject, message,'mum.amptech@gmail.com', recipient_list,html_message=html_message,fail_silently=False,)
