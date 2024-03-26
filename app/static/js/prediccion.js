/**
 * index.js
 * - All our useful JS goes here, awesome!
 */
window.onbeforeunload = function () {
    window.scrollTo(0, 0);
};

// Variabili
var $ = document.querySelector.bind(document);
var $$ = document.querySelectorAll.bind(document);
$titles = $$("#section-2 .section__title span");
var controller = new ScrollMagic.Controller();
var tl1 = new TimelineMax({paused:true}),
    tl2 = new TimelineMax();

// Timeline Tweenmax prima sezione
tl1
.from("#section-1 .section__title h2",1,{ y:1000 , opacity:1 , ease: Expo. easeOut },1)
    .to("#section-1 .section__title h2",0,{ y:0 , opacity:1 , ease: Expo. easeOut })
.from("#section-1 .section__text div",1,{ y:1000 , opacity:1 , ease: Expo. easeOut },1)
    .to("#section-1 .section__text div",0,{ y:0 , opacity:1 , ease: Expo. easeOut })
.fromTo("#section-1 .section-animate__left", 0.5, {css: {bottom: "100%"}}, {css:{bottom: "0"}},2)
.fromTo("#section-1 .section-animate__right", 0.5, {css: {top: "100%"}}, {css:{top: "0"}},2)
.from("#section-1 .reveal-bottom img",1,{ y:1000 , opacity:1 , ease: Expo. easeOut },"+=0.5")
    .to("#section-1 .reveal-bottom img",0,{ y:0 , opacity:1 , ease: Expo. easeOut })
.from("#section-1 .reveal-left img",1,{ x:-800 , opacity:1 , ease: Expo. easeOut },"+=0.5")
    .to("#section-1 .reveal-left img",0,{ x:0 , opacity:1 , ease: Expo. easeOut });

// Timeline Tweenmax seconda sezione
tl2
.staggerFromTo($titles, 1, { y:300 , opacity:1 , ease: Expo. easeOut },{ y:0 , opacity:1 , ease: Expo. easeOut }, 1)
.fromTo("#section-2 .reveal-left .cover", 0.5, {css: {left: "0"}}, {css:{left: "100%"}},"+=0.5")
.from("#section-2 .section__text p",2,{ x:-800 , opacity:0 , ease: Expo. easeOut },"-=1")
    .to("#section-2 .section__text p",2,{ x:0 , opacity:1 , ease: Expo. easeOut },"-=0.5");


// Attivazione Loader
$("#hide-page").style.display = "block";

// Al caricamento della pagina nasconde il loader e partono le animazioni
window.onload = function() {  
    $("#hide-page").style.display = "none";
    setTimeout(function(){ 
    tl1.play();
    }, 700);   
};

// Attivazioni animazioni allo scroll
var scene = new ScrollMagic.Scene({triggerElement: "#section-1"})
                            .setTween(tl1)
                            //.addIndicators()
                            .addTo(controller);
var scene2 = new ScrollMagic.Scene({triggerElement: "#section-2"})
                            .setTween(tl2)
                            .addTo(controller);

                            
function redirectTo(endpoint) {
    window.location.href = endpoint;
}