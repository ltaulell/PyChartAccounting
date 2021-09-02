$('button.toJpg').on('click', function(e){
    e.preventDefault();

    var node = document.getElementById(this.id);
    var name = this.id.replace("-img", "")
   
    domtoimage.toBlob(node).then(function (blob) {
        window.saveAs(blob, name+'.png');
    });

});
