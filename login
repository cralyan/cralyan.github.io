<!doctype html>
<html xmlns="http://www.w3.org/1999/html" xmlns="http://www.w3.org/1999/html">
<head>
	<meta charset='UTF-8'/>
	<title>login</title>
	<style>
		*{margin:0px;padding:0px}
		body{background:url({{url_for('static',filename='img/bckl.gif')}});}
		#main{
			margin:200px auto;
			width:40%;
			height:500px;
		}
		form {
		    font-size:20px;
		}
        form input{
            width:300px;
            height:30px;
            font-size:18px;
        }
</style>
</head>
<body>
	<div id='main' align='center'>
        <h1 style="color:green">登录中心</h1></br>
		<form method='post' action='' id='form' novalidate>
			{% if msg %} <h3><font style='color:#ff0000; font-weight: blod;'>{{msg}}</font></h3> {% endif %}
		    {% for item in form %}
            <p style="color:#fff">{{item.label}}: {{item}} </br><font style="color:red;font-weight:bold;font-size:17px">{{item.errors[0] }}</font></p></br></br>
            {% endfor %}
			<div class='submit' align='center'>
				</br><button type='submit' style="height:50px;width:100px;"><font style='font-size: 23px; color:#3333ff; '>&nbsp&nbsp 登 录&nbsp&nbsp</font></button>
			</div>
		</form>
	</div>
</body>
</html>
