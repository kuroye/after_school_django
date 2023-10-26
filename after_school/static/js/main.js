function nextBtn() {
    var x = document.getElementById("next-btn");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

(function ($) {
    $.fn.typewriter  = function() {
              this.each(function() {
                  var $ele = $(this), str = $ele.html(), progress = 0;
        $ele.show().html('');
                  var timer = setInterval(function() {
                      var current = str.substr(progress, 1);
         
                      if (current == '<') {
                          progress = str.indexOf('>', progress) + 1;
           
                      } else {
                          progress++;
                      }
                      if (progress >= str.length) {
                          
                          clearInterval(timer);
                          nextBtn();
                          console.log("I AM FINISHED");
                          
                      }
         $ele.html(str.substring(0, progress));
                  }, 30);
              });
              return this;
          };
  })(jQuery)
  
  $('.text-area').typewriter();

  console.log("IT WORKS");


