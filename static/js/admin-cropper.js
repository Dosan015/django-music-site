// admin base.html
// <link rel="stylesheet" type="text/css" href="{% static "css/cropper.min.css" %}">
//<script src="{% static 'js/jquery-3.6.0.min.js' %}" ></script>
//<script src="{% static 'js/cropper.min.js' %}" ></script>
//<script src="{% static 'js/jquery-cropper.min.js' %}" ></script>
//<script src="{% static 'js/admin-cropper.js' %}" ></script>
//
// app change_form.html
//<div id="image-box">
//</div>
//<input type="file" name="img" accept="image/*" id="id_image">
//<button id="confirim-btn" >Сақтау</button>
// As a global Object

var jsmediatags = window.jsmediatags;
const imageBox = document.getElementById('image-box')
const cBtn = document.getElementById('confirim-btn')
const idimg = document.getElementById('id_img')
const file = document.getElementById('id_file')
const title = document.getElementById('id_name')

if (file != null) {
file.addEventListener('change', (e)=> {
	const mp3_data = file.files[0]
	jsmediatags.read(mp3_data, {
		onSuccess: function(tag) {
			document.getElementById('id_name').value = tag.tags.title
			var select = document.getElementById('id_singer')
			for (let i = 0; i < select.length; i++) {
				if (select[i].text === tag.tags.artist) {
					select.value = select[i].value
					break
				}

			}
		},
		onError: function(error) {
			alert(error);
		}
	});
	e.preventDefault();
});
}


var cropper
if (!$) {
    //$ = django.jQuery;
    alert('jQuery not Found')
}
console.log('&&***')
idimg.addEventListener('change', ()=> {
	const img_data = idimg.files[0]
	const url = URL.createObjectURL(img_data)
	imageBox.innerHTML = `<img src="${url}" id="image" width="500px">`
    cBtn.style.display = "block";
    var $image = $('#image');

    $image.cropper({
    aspectRatio: 12 / 9,
});


cropper = $image.data('cropper');
})

cBtn.addEventListener('click', (e) => {
	cropper.getCroppedCanvas().toBlob((blob) => {
		var dataTransfer = new ClipboardEvent('').clipboardData || new DataTransfer();
		dataTransfer.items.add(new File([blob], 'new-image.png'));
		var inputElement= document.getElementById('id_img')
		inputElement.files = dataTransfer.files;
    });
    imageBox.remove()
    cBtn.style.display = "none";
    e.preventDefault();
})



