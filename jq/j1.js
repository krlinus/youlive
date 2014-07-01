function ping1() {
  //alert('ping called');
  var xmlhttp;
  if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
  }
  else
  {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange=function() {
      if (xmlhttp.readyState==4 && xmlhttp.status==200)
      {
        //document.getElementById("myDiv").innerHTML+="In good place";
        document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
      }
      else
      {
        document.getElementById("myDiv").innerHTML+="Failure";
      }
    }
  xmlhttp.open("POST","q1.php",true);
  xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  xmlhttp.send("name=Henry");
  
}

