
$(document).on('change', '#browsebutton :file', function() {
    console.log("event ------ browsebutton change");
    var input = $(this);
    getFileName(input);
    console.log("event end ------ browsebutton change");
});

$(document).ready( function() {  
    $('#cropForm').submit(($e) => {
        console.log("event ------ cropForm Submit Clicked");
        $e.preventDefault();
        cropImage(crop);
        var overlay = $("#overlay-container");
        cleanPopup(overlay);
        refreshPopup(overlay);
        crop.destroy();
        console.log("   Croppie Instance Destroyed");
        console.log("event end ------ browsebutton change");
        });
    
    $('#browsebutton :file').on('fileselect', function(event, numFiles, filename) {
        /* Setting the path truncated file name into "test_input" text box */
        console.log("event ------ browsebutton fileselect");
        var crop = croppieInit();
        console.log("   Crop: " + crop);
        var input = $(this).parents('.input-group.active').find('.text'),
        fileName = numFiles > 1 ? numFiles + ' files selected' : filename;
        if( input.length ) {
            } else {
                if( fileName ) {
                    document.getElementById("image_name").value = fileName;
                }
        }
        $(".popup-overlay").addClass("active");
        var reader = new FileReader();
        reader.onload = function () {
            console.log("   FileReader Loaded");
            var dataURL = reader.result;
            var imageSrc = document.getElementById('imageSrc');
            imageSrc.src = dataURL;
            $('#imageSrc').val(dataURL);
            croppieBind(crop, dataURL);
        };
        console.log("   reader.readAsDataURL: " + $(this)[0].files[0]);
        // console.log($(this)[0].files[0]);
        reader.readAsDataURL($(this)[0].files[0]);
        console.log("event end ------ browsebutton fileselect");
    });
    
    $("#cropbtn").on("click", function() {
        console.log("event ------ cropbtn Crop Clicked");
        console.log("   Crop: " + crop);
        cropImage(crop);
        var overlay = $("#overlay-container");
        cleanPopup(overlay);
        refreshPopup(overlay);
        crop.destroy();
        console.log("   Croppie Instance Destroyed");
        console.log("event end ------ cropbtn Crop Clicked");
    });

    $("#cancelbtn").on("click", function() {
        console.log("event ------ Cancel Clicked");
        location.reload();
        console.log("event end ------ Cancel Clicked");
    });
});

/* Functions */
function getFileName(input){
    console.log("func >>>>>> In getFileName");
    numFiles = input.get(0).files ? input.get(0).files.length : 1;
    filename = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, filename]);
    console.log("func <<<<<< Out getFileName");
}

function cropImage(crop) {
    console.log("func >>>>>> In cropImage");
    console.log("   Crop: " + crop);
    results = crop.get();
    $('#outX1').val(results.points[0]);
    $('#outY1').val(results.points[1]);
    $('#outX2').val(results.points[2]);
    $('#outY2').val(results.points[3]);
    var canvas = document.getElementById('myCanvas');
    var context = canvas.getContext('2d');
    var imageSrc = document.getElementById('imageSrc');
    var dX1 = document.getElementById("outX1").value;
    var dY1 = document.getElementById("outY1").value;
    var dX2 = document.getElementById("outX2").value;
    var dY2 = document.getElementById("outY2").value;
    console.log("   dX1: " + dX1);
    console.log("   dY1: " + dY1);
    console.log("   dX2: " + dX2);
    console.log("   dY2: " + dY2);
    var w = dX2 - dX1;
    var h = dY2 - dY1;
    console.log("   H: " + h + " W: " + w);
    var dWidth = dX2 - dX1;
    var dHeight = dY2 - dY1;
    var hRatio = canvas.width / dWidth;
    var vRatio = canvas.height / dHeight;
    var ratio = Math.min(hRatio, vRatio);
    console.log("   hRatio: " + hRatio);
    console.log("   vRatio: " + vRatio);
    console.log("   ratio: " + ratio);
    context.drawImage(imageSrc, dX1, dY1, dWidth, dHeight, 0, 0, dWidth * ratio, dHeight * ratio);
    console.log("func <<<<<< Out cropImage");
}

function cleanPopup(overlay) {
    console.log("func >>>>>> In cleanPopup");
    $(".popup-overlay").removeClass("active");
    overlay.empty();
    console.log("func <<<<<< Out cleanPopup");
}

function refreshPopup(overlay) {
    console.log("func >>>>>> In refreshPopup");
    overlay.append('<div id="image-holder"></div>');
    overlay.append('<div><input class="btn btn-primary" id="cropbtn" name="crop" type="submit" value="Click to complete Crop!"><button type="button" value="Button" id="cancelbtn">Cancel</button></div>');
    console.log("func <<<<<< Out refreshPopup");
}

function croppieBind(crop, path) {
    console.log("func >>>>>> In croppieBind");
    crop.bind({
        url: path,
        zoom: 0.85
    });
    console.log("func <<<<<< Out croppieBind");
}

function croppieInit() {
    console.log("func >>>>>> In croppieInit");
    vEl = document.getElementById('image-holder')
    console.log("func <<<<<< Out croppieInit");
    return crop = new Croppie(vEl, {
        enableExif: true,
        viewport: {
            width: 360,
            height: 450
        },
        boundary: {
            width: 600,
            height: 600
        }        
    });    
}




