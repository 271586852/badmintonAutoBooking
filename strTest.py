import re

def extract_and_respond(html_content):
    # Regular expression to extract Chinese characters
    chinese_text = "".join(re.findall(r'[\u4e00-\u9fff]+', html_content))
    
    # Check for the specific message
    if "该预约日期暂未开放预约" in chinese_text:
        return "暂未开放预约，重试中"
    else:
        return chinese_text

# Example HTML content
html_content = """
getOpeningRoomError:  <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>系统异常</title>
</head>
<body>
    <div>该预约日期暂未开放预约</div>
</body>
</html>
"""

# Call the function with the example HTML content
# Uncomment below to test:
print(extract_and_respond(html_content))
