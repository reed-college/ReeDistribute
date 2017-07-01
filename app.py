{% extends "basic.html" %}
{% block content %}
<!DOCTYPE html>
<html>
  <head>
    <title>ReeDistribute</title>
    <style type="text/css" media="screen">
  form {
      padding-left:25%;
      padding-right:25%;
  }
  button.accordion {
    background-color: #eee;
    color: #444;
    cursor: pointer;
    padding: 16px;
    width: 50%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 15px;
    transition: 0.4s;
  }

  button.accordion.active, button.accordion:hover {
      background-color: #ddd;
  }

  button.accordion:after {
      content: '\002B';
      color: #777;
      font-weight: bold;
      float: right;
      margin-left: 5px;
  }

  button.accordion.active:after {
      content: "\2212";
  }

  div.panel {
      padding: 0 18px;
      background-color: white;
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.2s ease-out;
  }
  body {
    background-color: #ffda56;
    margin: 1;
    position: absolute;
    right: 0;
    bottom: 0;
    left: 0;
    padding: 1.5rem;
    background-color: #efefef;
    text-align: center;
    color: #9b0700;
  }
    #when {
      font-size:11px;
    }
    #entry {
      background-color: #efefef;
      border: 3px solid #f1f1f1;
      color: black;
    }
    #who {
      font-size:11px;
      color:black;
    }
    #uuid, #uuid2 {
      visibility: hidden;
    }
    h2 {
      text-align: center;
      float:center;
    }
    h4 { 
      display:inline;
      text-align: left
      color:#9b0700;
    }

</style>
</head>
<p>
<?xml version="1.0" encoding="utf-8"?>
<body>
<feed xmlns="http://www.w3.org/2005/Atom">
<h2>Example Feed</h2>
<button class="accordion"><post-title style="font-size:20px"> I need this </post-title><br><author class="who" style="font-size: 11px">John Doe </author></button>
  <div class="panel">
  <br>
  <updated id="when">2003-12-13T18:30:02</updated>
  <br>
  <id id="uuid">urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>
  <br>
    <entry id="entry" type="container" style="background-color: #efefef; display:inline-block; margin:auto; text-align: center;">
      <span name="post">One Example Request</span> <br>
      <!-- post name will be referencing the database -->

      <id id=uuid2>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
      <!-- this will be referencing the ID number, hidden right now -->
      <span class="desc" style="float:center;">Some text.</summary>
      <!-- database's description text. Should we create a character limit for this? (yes) (like 1000 words right?) -->
      <form action="/charge" method="POST">
      <!-- this charges the customer -->
      <span class="amount" style="display:block;">$<input type="value" class="amount" required></span>
      <br>
      <h4>
      <form action="/charge" method="POST">
      <script
      src="https://checkout.stripe.com/checkout.js" class="stripe-button"
      data-key="pk_test_KovI8IiKzzuFbk33ewAjbYzc" 
      data-name="example rqst"
      data-image="https://www.hscripts.com/freeimages/logos/academic-institution-logos/reed-college-griffin/reed-college-griffin-256.gif"
      data-locale="auto">
      </script>
      <!-- stripe API, data-name and data-desc should be a variable -->
      </form>
      </h4>
      </form>
    </entry>
</feed>
</p>
</div>
</body>

</div>
<script>
var amt_donate = document.getElementsByClassName("amount");
var desc = document.getElementsByClassName("desc");
var author = document.getElementsByClassName("who");
// make the amount, desc, and author variables-- right now it's examples (db)

</script>
<script>
var acc = document.getElementsByClassName("accordion");
var i;
for (i = 0; i < acc.length; i++) {
  acc[i].onclick = function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  }
}
</script>
{% endblock %}
