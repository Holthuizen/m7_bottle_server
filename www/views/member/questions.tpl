<!DOCTYPE html>
<html>
<body>


<h2> List of questions, open and closed </a> </h2> 

<p></p>

<hr>
<table>
  %for item in data:
    Title: <b> {{item['Title']}} </b>
    <br/>
    Decription: <b> {{item["description"]}} </b>
    <br/>
    Question: <b> {{item["question"]}} </b>
    <br/>
    published at : <b> {{item['published_at']}} </b>
    <br/>
    published by:  <b> {{item['author'][0]['username']}} </b>
    <br/>
    Subjects:
    %for category in item['categories']: 
         <ul>
            <li>{{category['Subject']}}</li>
         </ul>
    %end
    <br/>
    <hr>
  %end
</table>

<br> 


</body>
</html>
