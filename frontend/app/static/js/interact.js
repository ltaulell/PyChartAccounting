$('button.toJpg').on('click', function(e){
    e.preventDefault();
    console.log(this.id);
    window.scrollTo(0,0);  
    html2canvas($("#"+this.id)[0], {scrollY: -window.scrollY}).then((canvas) => {
        console.log("done ... ");
        document.body.appendChild(canvas);

        canvas.toBlob(function(blob) {
            saveAs(blob, "img.jpg"); 
        });
    });

});