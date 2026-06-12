
(function(){
  var THEMES=["light","sepia","dark"];
  var root=document.documentElement;

  // restore prefs
  try{
    var t=localStorage.getItem("ccg-theme"); if(t&&THEMES.indexOf(t)>=0) root.setAttribute("data-theme",t);
    var f=parseFloat(localStorage.getItem("ccg-fs")); if(f&&f>=0.85&&f<=1.6) root.style.setProperty("--fs",f+"rem");
  }catch(e){}

  function curFs(){
    var v=getComputedStyle(root).getPropertyValue("--fs");
    var n=parseFloat(v); return isNaN(n)?1.18:n;
  }
  function setFs(n){ n=Math.max(0.9,Math.min(1.55,n)); root.style.setProperty("--fs",n+"rem"); try{localStorage.setItem("ccg-fs",n);}catch(e){} }
  function cycleTheme(){
    var cur=root.getAttribute("data-theme")||"sepia";
    var next=THEMES[(THEMES.indexOf(cur)+1)%THEMES.length];
    root.setAttribute("data-theme",next);
    try{localStorage.setItem("ccg-theme",next);}catch(e){}
  }

  document.addEventListener("click",function(e){
    var b=e.target.closest("[data-action]"); if(!b) return;
    var a=b.getAttribute("data-action");
    if(a==="theme") cycleTheme();
    else if(a==="font-inc") setFs(curFs()+0.06);
    else if(a==="font-dec") setFs(curFs()-0.06);
  });

  // reading progress
  var bar=document.getElementById("progress-bar");
  function onScroll(){
    if(!bar) return;
    var h=document.documentElement;
    var max=(h.scrollHeight-h.clientHeight);
    var p=max>0?(h.scrollTop/max)*100:0;
    bar.style.width=p+"%";
  }
  document.addEventListener("scroll",onScroll,{passive:true});
  window.addEventListener("resize",onScroll); onScroll();

  // keyboard nav
  var art=document.querySelector(".chapter");
  document.addEventListener("keydown",function(e){
    if(e.target.matches("input,textarea")) return;
    if(e.key==="t"||e.key==="T"){ cycleTheme(); return; }
    if(e.key==="+"||e.key==="="){ setFs(curFs()+0.06); return; }
    if(e.key==="-"||e.key==="_"){ setFs(curFs()-0.06); return; }
    if(e.key==="Escape"){ window.location.href="index.html"; return; }
    if(!art) return;
    var prev=art.getAttribute("data-prev"), next=art.getAttribute("data-next");
    if((e.key==="ArrowRight")&&next){ window.location.href=next; }
    if((e.key==="ArrowLeft")&&prev){ window.location.href=prev; }
  });

  // remember last-read chapter for a "continue" hint on the index
  try{
    if(art){
      var slug=location.pathname.split("/").pop();
      localStorage.setItem("ccg-last",slug);
    }else{
      var last=localStorage.getItem("ccg-last");
      if(last){
        var link=document.querySelector('.toc-list a[href="'+last+'"]');
        if(link){ link.classList.add("last-read"); link.setAttribute("title","Last read"); }
      }
    }
  }catch(e){}
})();
