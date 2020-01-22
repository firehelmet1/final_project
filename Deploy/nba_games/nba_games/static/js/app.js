function buildMetadataHome(placehold) {
// placehold defined in function below in init function as HomeSample
  // Use `d3.json` to fetch the metadata for a sample
  var url = `/metadata/${placehold}`;
    // Use d3 to select the panel with id of `#sample-metadata`
    var sample_metadata_tableHome = d3.select("#sample-metadataHome");
    var teamLogo_Home = d3.select("#teamLogo_Home");
    var bgStyle = d3.select("#bgStyle");

    // console.log(sample_metadata_tableHome)
    // console.log(teamLogo_Home)

    // Use `.html("") to clear any existing metadata
    sample_metadata_tableHome.html("");
    teamLogo_Home.html("");
    bgStyle.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    d3.json(url).then((data) => {
      // var span = sample_metadata_table.append("span");
      Object.entries(data).forEach(([key, value]) => {
        var cell = sample_metadata_tableHome.append("li");
        cell.text(key + ": " + value);

      });
      // Object.entries(data).forEach(([key, value]) => {
        const obj = Object.entries(data)[0];
        var div = teamLogo_Home.append("img");
        div.attr("src", "../static/Images/Logos/" + obj[1] + ".png");
        div.attr("style", "width:88%" );
        var text = bgStyle.append("style");
        text.text("body {background-image: url('../static/Images/Courts/" + obj[1] + ".jpg'), url('../static/Images/Gymfloor_sm.jpg');}");
        // style.attr("url",'../static/Images/Gymfloor1.jpg');
        // console.log(obj[1]); 
        homeTeam = obj[1];
        // console.log(homeTeam);

    });
}

// Submit Button handler
function predictHandler() {
  const predictSampleH =document.getElementById("selDatasetHome").value;
  const predictSampleA =document.getElementById("selDatasetAway").value;
  
  // var url = `/metadata/${predictSample}`;
  var urlH = `/metadata/${predictSampleH}`;
  var urlA = `/metadata/${predictSampleA}`;
  // var metaData = url;
  // var sound0 = new Audio('../static/Images/AtTheBuzer.mp3'); 

  // Fetch the JSON data and console log it
  // .then is Asynchronus call to request the data and keep going while waiting for data
  d3.json(urlH).then((data) => {
    // console.log("HE SHOOTS HE SCORES");
    const obj = Object.entries(data)[0];
    // console.log(obj[1]);
    d3.json(urlH).then((data) => {
      const obj = Object.entries(data)[0];
      // console.log(obj[1]);
      home = obj[1];
      myFunction(home, away);
  });
  d3.json(urlA).then((data) => {
      const obj = Object.entries(data)[0];
      // console.log(obj[1]);
      away = obj[1];
    
});
var sound0 = new Audio('../static/Images/heShoots.mp4'); 

      if(obj[1] == 'BOS'){
      // if(obj[1]){

          console.log("VEGAS BABY");
          sound0.volume = 0.14;
          sound0.play();  
      }
  });

    const HomeSample =document.getElementById("selDatasetHome").value;
    const AwaySample =document.getElementById("selDatasetAway").value;

    var urlH = `/metadata/${HomeSample}`;
    var urlA = `/metadata/${AwaySample}`;
    // console.log(urlH, urlA);
      d3.json(urlH).then((data) => {
          const obj = Object.entries(data)[0];
          // console.log(obj[1]);
          home = obj[1];
          // myFunction(home, away);
      });
      d3.json(urlA).then((data) => {
        const obj = Object.entries(data)[0];
        // console.log(obj[1]);
        away = obj[1];
        
    });
    
    // });
  }
  home = '';
// Snackbar Handler
function myFunction(home, away) {

  var sound0 = new Audio('../static/Images/AtTheBuzer.mp3'); 
  // console.log("VEGAS BABY");
  sound0.volume = 0.1;
  sound0.play();  
 
  // Predict Winner
  var urlPredictor = `/predictor/${home}/${away}`;
  // console.log(urlPredictor);
  d3.json(urlPredictor).then((data) => {
    const obj = Object.entries(data)[0];
    const obj1 = Object.entries(data)[1];
    const obj2 = Object.entries(data)[2];
    const obj3 = Object.entries(data)[3];


    // console.log(obj[1]);
    points_total = obj[1].toFixed(1);;
    winner = obj1[1];
    score = obj2[1].toFixed(2);
    spread = obj3[1].toFixed(2);


    console.log("The winner is: " + winner +" R2 score: "+ score);

  // Get the snackbar DIV
  // console.log(home, away);

  var x = document.getElementById("snackbar")
  var y = document.getElementById("snackbar").innerHTML = winner +" WINS "+'<br>'+" R2 score: "+ score;
  
  var div = document.getElementById("snackbar").innerHTML = 
  "<img src="+  "../static/Images/Logos/" + winner + ".png>" +"<br>" + winner +" WINS "+'<br>'+"R2 score: "+ score +'<br>'+"Spread: "+ spread +'<br>'+"Points Total: "+ points_total ;  
  
  // div.attr("src", "../static/Images/Logos/" + "ATL" + ".png");
  // div.attr("style", "width:80%" );

  // Add the "show" class to DIV
  x.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 4000);


    // myFunction(home, away);
});
  
}


function buildMetadataAway(placehold) {
// placehold defined in function below in init function as AwaySample

  // Use `d3.json` to fetch the metadata for a sample
  var url = `/metadata/${placehold}`;

    // Use d3 to select the panel with id of `#sample-metadata`
    var sample_metadata_tableAway = d3.select("#sample-metadataAway");
    var teamLogo_Away = d3.select("#teamLogo_Away");
    // console.log(sample_metadata_tableHome)
    // console.log(teamLogo_Home)

    // Use `.html("") to clear any existing metadata
    sample_metadata_tableAway.html("");
    teamLogo_Away.html("");
    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.

    d3.json(url).then((data) => {
      // var span = sample_metadata_table.append("span");
      Object.entries(data).forEach(([key, value]) => {
        var cell = sample_metadata_tableAway.append("li");
        cell.text(key + ": " + value);

      });
      // Object.entries(data).forEach(([key, value]) => {
        const obj = Object.entries(data)[0];
        var div = teamLogo_Away.append("img");
        div.attr("src", "../static/Images/Logos/" + obj[1] + ".png");
        div.attr("style", "width:88%" );
        // console.log(Object.entries(data)[0]); 
        // console.log(obj[1]); 

      // });
      
    });
    
}

function init() {
  // Grab a reference to the dropdown select element
  var selectorH = d3.select("#selDatasetHome");
  var selectorA = d3.select("#selDatasetAway");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNamesHome) => {
    sampleNamesHome.forEach((sample) => {
      selectorH
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const HomeSample = sampleNamesHome[0];

    // buildCharts(firstSample);
    buildMetadataHome(HomeSample);

  });
  d3.json("/names").then((sampleNamesAway) => {
    sampleNamesAway.forEach((sample) => {
      selectorA
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const AwaySample = sampleNamesAway[0];

    // buildCharts(firstSample);
    buildMetadataAway(AwaySample);

  });

}

function optionChangedHome(newSample) {
  // Fetch new data each time a new sample is selected
  // buildCharts(newSample);
  buildMetadataHome(newSample);
  // console.log(newSample)
}
function optionChangedAway(newSample) {
  // Fetch new data each time a new sample is selected
  // buildCharts(newSample);
  buildMetadataAway(newSample);
}


// Initialize the dashboard
init();
