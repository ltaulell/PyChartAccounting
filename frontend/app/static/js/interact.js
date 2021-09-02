$('button.toJpg').on('click', function(e){
    e.preventDefault();
    html2canvas($("#"+this.id)[0], {
        scale: 5
      }).then((canvas) => {
        document.getElementById("imgSave").appendChild(canvas);

        canvas.toBlob(function(blob) {
            saveAs(blob, "img.jpg"); 
        });
    });

});