var submit= document.querySelector('#submit-btn')
var inpfile= document.querySelector('#input-file')
var inputhid=document.querySelector('#inputhid')
var inpnum= document.querySelector('#input-number')
var msg= document.querySelector('#msg')
var my_form= document.querySelector('#myform')
var radioelm= document.querySelectorAll('input[name="image_type"]')
var radiobox=document.getElementById('8')

var cancel=document.getElementById('cancel')
const video = document.querySelector('#avideo');
var canvas = document.querySelector('#acanvas');
const snap = document.querySelector("#snap");
const errorMsgElement = document.querySelector('span#errorMsg');
var tracks =null;
const constraints = {
    audio: false,
    video: {
        width: 800, height: 500
    }
};

snap.style.display='none';
cancel.style.display='none';

// console.log("imgtype form ele",my_form.elements['image_type'])

my_form.addEventListener('submit',on_submit);

radiobox.addEventListener('change', init);

cancel.addEventListener('click',(e)=>{
    setTimeout(() => {video.style.display= 'none'; tracks.forEach(function(track) {
        track.stop();
    });})
} 
)

function on_submit(ev){
    ev.preventDefault();
    if(inpfile.value =='' && inputhid.value !=''){
        console.log("input value cam", inputhid.value)
        console.log("input value cam", my_form.elements['image_type'].value)
        msg.style.display='inline'
        msg.innerHTML=`<p>image captured,please press predict</p>`;
        setTimeout(()=> msg.style.display='none', 3000);
        // setTimeout(()=> {submit.classList.remove('subm-btn'); submit.value='Predict';}, 2000);
        // //my_form.action='/submit'
        my_form.submit();

        radioelm.forEach(function(elm) {
            elm.checked = false;
          })
        inpfile.value='';
    }
    else if(inpfile.value ==''  || my_form.elements['image_type'].value ==''){
        
        submit.classList.add('error')
        msg.style.display='inline-block'
        msg.classList.add('error')
        msg.innerHTML=`<p>please provide all the details</p>`
        setTimeout(()=> {msg.style.display='none';}, 3000);
        setTimeout(()=> {submit.classList.remove('error');}, 3000);
        setTimeout(()=> {msg.classList.remove('error'); radioelm.forEach(function(elm) {
            elm.checked = false;
          });}, 3000
          );
         
    }
    else{
        submit.classList.add('subm-btn');
        submit.value='loading'
        msg.style.display='inline'
        msg.innerHTML=`<p>your file ${inpfile.value} has been loaded</p>`;
        setTimeout(()=> msg.style.display='none', 3000);
        setTimeout(()=> {submit.classList.remove('subm-btn'); submit.value='Predict';}, 2000);
        //my_form.action='/submit'
        my_form.submit();

        radioelm.forEach(function(elm) {
            elm.checked = false;
          })
        inpfile.value='';
        
        
    }
}
var context = canvas.getContext('2d');
snap.addEventListener("click", function() {
    context.drawImage(video, 0, 0, 640, 480);
    setTimeout(() => {video.style.display= 'none'; tracks.forEach(function(track) {
        track.stop();
    });snap.style.display='none';
    cancel.style.display='none';},2000)
} );   


function handleSuccess(stream) {
    window.stream = stream;
    video.srcObject = stream;
    tracks= stream.getTracks();
}


// Access webcam
async function inits() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        console.log("STREAM: I could run!")
        handleSuccess(stream);
            
    } catch (e) {
        errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
    }
}

function init(ev){
    
    inits();
    snap.style.display='inline';
    cancel.style.display='inline';
    snap.addEventListener("click", function() {
        inputhid.value=canvas.toDataURL('image/png').split("base64,")[1].toString();
        console.log("inputhid.value",typeof inputhid.value)
        my_form.elements['image_type'].value = 5;
        my_form.action='/submitlive'
        // my_form.submit();
    })
    //my_form.elements['image_type'].value = 5;
    
    // my_form.action='/submitlive'
    // my_form.submit();

}


// Draw image

