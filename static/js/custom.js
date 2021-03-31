(() => {
  console.log("page loaded");
  // $("#navbarDropdown").mouseover(function(){
  //     $('#navbarDropdown2').parent().parent().show();
  //     $('#navbarDropdown2').next().show();
  //     // $('#navbarDropdown1').parent().addClass('dropdown show');//.click();
  //     // $('#navbarDropdown2').click();
  //   });
  //   $('#navbarDropdown1').click(function(){

  //   });
  $(".exdrop>li").hover(
    function () {
    $(this).find('ul:eq(0)').show();
    $(this).find('ul:eq(0) li:eq(0) ul:eq(0)').show();
    },
    function () {
      $(this).find('ul:eq(0)').hide();
      $(this).find('ul:eq(0) li:eq(0) ul:eq(0)').hide();
    }
  );
  $(".exdrop2>li").hover(
    function () {
    $(this).find('ul:eq(0)').show();
    },
    function () {
      $(this).find('ul:eq(0)').hide();
    }
  );
  $("#navbarDropdown").hover(
    function () {
    $(this).next().find('ul:eq(0)').show();
    $(this).next().find('ul:eq(0) li:eq(0) ul:eq(0)').show();
    },
    function () {
      $(this).next().find('ul:eq(0)').hide();
      $(this).next().find('ul:eq(0) li:eq(0) ul:eq(0)').hide();
    }
  );

  // $("#navbarDropdown2").hover(
  //   function () {
  //     $("#navbarDropdown2").next().show();
  //   },

  //   function () {
  //     $("#navbarDropdown2").next().hide();
  //   }
  // );
})($);
// function ChangesView(d){
//     $(d).find('ul:eq(0)').show();
//     $(d).find('.masterbox').show();
// }
$(document).ready(function() {

  $('.accordion-item__trigger').click(function() {
      $('.accordion-item__content').slideToggle('accordion-item__content-active')
  });

});