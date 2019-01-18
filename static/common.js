var v=0;
var xmlhttp;
function f5 ()
{
  //alert('in f5 state ' + xmlhttp.readyState);
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
  {
    var obj=eval('('+xmlhttp.responseText+')');
    var tabStr="";
    var i=0;
    th_str='<tr><th colspan=3 align="left">My Header</th></tr>';
    for (n in obj)
    {
      if((i==0) || (i %3 == 0))
        tabStr += "<tr>";

      tabStr += '<td><img src="' + obj[n] + '" /></td>';
      if((i!=0) && (i %3) == 2)
        tabStr += "</tr>";
      i++;
    }
    if((i==0) || (i %3) != 2)
        tabStr += "</tr>";
    //alert(tabStr);
    document.getElementById("t1").innerHTML=th_str+tabStr;

  }
}
function begin ()
{
  //document.getElementById("txtHint2").innerHTML='begin ' + v;
  v++;
  if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
  }
  else
  {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  var str=document.getElementById("txtHint").innerHTML;
  xmlhttp.open("GET","/f5handle?q="+encodeURI(str),true);
  xmlhttp.onreadystatechange=f5;
  xmlhttp.send();
  setTimeout("begin()",15000);
}
