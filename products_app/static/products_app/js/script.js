$(function() {
    console.log("loaded");
    $('.floppy-green').parent().prop('title','Bookmark this product')
    $('.floppy-red').parent().prop('title','Already Bookmarked - Click to remove');

    $('.fa-save').click(function(e){
        let data = {};
        if ($(this).hasClass('floppy-green')){
            data['action'] = "add"
            $(this).parent().prop('title','Already Bookmarked - Click to remove');
        } else {
            data['action'] = "remove"
            $(this).parent().prop('title','Bookmark this product');
        }
        $(this).toggleClass('floppy-green')
        $(this).toggleClass('floppy-red')
        let barcodes = this.id;
        let pos = barcodes.indexOf("-");
        let subst_barcode=barcodes.substr(0,pos);
        let prod_barcode=barcodes.substr(pos+1);
        data['subst'] = subst_barcode;
        data['prod'] = prod_barcode;
        data = JSON.stringify(data);
        SendAjax('POST','save_remove_bookmark/',data)
            .done( function(response) {

            })
            .fail( function(response) {
                console.error("Erreur Ajax : " + response.data);
                alert("Erreur Ajax - "+ response.data);
            });
    });
});



let SendAjax = function(type=post ,url, data, datatype='json', contenttype='application/json' ){
    /*
    Send ajax request to server 
    */
    return $.ajax({
        type: type,
        url: url,
        data: data,
        dataType: datatype,
        contentType: contenttype,
    })
}; 