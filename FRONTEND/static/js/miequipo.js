var players =  [{
    name: 'Pizarro',
    asset: 'bm-pizarro.jpg',
    origin: 'Peru',
    height: '1.84m',
    shirt: '14',
    pos: 'Forward',
    dob: '36',
    goals: 1,
    games: 16,
    x: 110,
    y: -190
  }, {
    name: 'Pizarro',
    asset: 'bm-pizarro.jpg',
    origin: 'Peru',
    height: '1.84m',
    shirt: '14',
    pos: 'Forward',
    dob: '36',
    goals: 1,
    games: 16,
    x: 110,
    y: -190
  }, {
    name: 'Robben',
    asset: 'bm-robben.png',
    origin: 'Holland',
    height: '1.80m',
    shirt: '10',
    pos: 'Forward',
    dob: '32',
    goals: 19,
    games: 30,
    x: -110,
    y: -190
  }, {
    name: 'Rilbery',
    asset: 'bm-rilbery.jpg',
    origin: 'France',
    height: '1.70m',
    shirt: '7',
    pos: 'Midfield',
    dob: '32',
    goals: 9,
    games: 22,
    x: 150,
    y: 50
  }, {
    name: 'Schweinsteiger',
    asset: 'bm-schweinsteiger.jpg',
    origin: 'Germany',
    height: '1.87m',
    shirt: '24',
    pos: 'Forward',
    dob: '31',
    goals: 21,
    games: 3,
    x: 0,
    y: 100
  }, {
    name: 'Martinez',
    asset: 'bm-martinez.jpg',
    origin: 'Spain',
    height: '1.90m',
    shirt: '8',
    pos: 'Midfield',
    dob: '28',
    goals: 0,
    games: 2,
    x: -150,
    y: 50
  }, {
    name: 'Alaba',
    asset: 'bm-alaba.jpg',
    origin: 'Austria',
    height: '1.80m',
    shirt: '27',
    pos: 'Defence',
    dob: '24',
    goals: 5,
    games: 27,
    x: -200,
    y: 180
  }, {
    name: 'Lahm',
    asset: 'bm-lahm.jpg',
    origin: 'Germany',
    height: '1.70',
    shirt: '21',
    pos: 'Defence',
    dob: '32',
    goals: 2,
    games: 25,
    x: 200,
    y: 180
  }, {
    name: 'Benatia',
    asset: 'bm-benatia.jpg',
    origin: 'France',
    height: '1.87m',
    shirt: '5',
    pos: 'Defence',
    dob: '31',
    goals: 21,
    games: 1,
    x: 100,
    y: 300
  }, {
    name: 'Dante',
    asset: 'bm-dante.jpg',
    origin: 'Brazil',
    height: '1.87m',
    shirt: '4',
    pos: 'Defence',
    dob: '32',
    goals: 0,
    games: 34,
    x: -100,
    y: 300
  }, {
    name: 'Neuer',
    asset: 'bm-neuer.jpg',
    origin: 'Germany',
    height: '1.93m',
    shirt: '1',
    pos: 'Goalie',
    dob: '29',
    goals: 0,
    games: 48,
    x: 0,
    y: 410
  }];
  
  var team = document.getElementsByClassName("team")[0];
  players.forEach(function(el, index){
    nodePlayer = document.createElement("div");
    nodePlayer.classList.add("player");
    nodePlayer.style.display = "block";
    nodePlayer.style.opacity = "1";
    nodePlayer.style.transform = "translateX(" + el.x + "px) translateZ(" + el.y + "px)";
    team.appendChild(nodePlayer);
    //------------  
    node = document.createElement("div");
    node.classList.add("player__placeholder");
    nodePlayer.appendChild(node);
    node = document.createElement("div");
    node.classList.add("player__card");
    nodePlayer.appendChild(node);
    nodeH3 = document.createElement("h3");
    nodeH3.innerText = el.name;
    node.appendChild(nodeH3); 
    //------------  
    nodeUl = document.createElement("ul");
    nodeUl.classList.add("player__card__list");
    node.appendChild(nodeUl);
    nodeLi = document.createElement("li");
    nodeLi.innerHTML = "DOB<br>" + el.dob;
    nodeUl.appendChild(nodeLi);
    nodeLi = document.createElement("li");
    nodeLi.innerHTML = "Height<br>" + el.height;
    nodeUl.appendChild(nodeLi);
    nodeLi = document.createElement("li");
    nodeLi.innerHTML = "Origin<br>" + el.origin;
    nodeUl.appendChild(nodeLi);
    //------------
    nodeUl = document.createElement("ul");
    nodeUl.classList.add("player__card__list", "player__card__list--last");
    node.appendChild(nodeUl);
    nodeLi = document.createElement("li");
    nodeLi.innerHTML = "<span>Games</span><br>" + el.games;
    nodeUl.appendChild(nodeLi);
    nodeLi = document.createElement("li");
    nodeLi.innerHTML = "<span>Goals</span><br>" + el.goals;
    nodeUl.appendChild(nodeLi);
    //------------
    node = document.createElement("div");
    node.classList.add("player__label");
    node.style.display = "block";
    node.style.opacity = "1";
    node.innerHTML = "<span>" + el.name + "</span>";
    nodePlayer.appendChild(node);
    //------------
    node = document.createElement("div");
    node.classList.add("player__img"); 
    nodeImg = document.createElement("img");
    nodeImg.src = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/215059/" + el.asset;
    node.appendChild(nodeImg);
    nodePlayer.appendChild(node);
  });
  
  
  document.addEventListener('DOMContentLoaded', function () {
    [].forEach.call(document.getElementsByClassName("player"), function(el) {
      el.addEventListener("click", function(ev){
        var container = ev.currentTarget;
        var objCard = container.querySelector(".player__card");
        objCard.style.height = "260px";
        var objLabel = container.querySelector(".player__label");
        var objImg = container.querySelector(".player__img");
        if(container.classList.contains("active")){
          container.classList.remove("active");
          objCard.style.display = "none";
          objCard.style.opacity = "0";
          objLabel.style.opacity = "1";
          objImg.style.transform = "translateY(0px)";
        }else{
          var element = document.querySelector(".player.active");
          if (element != null){
            element.classList.remove("active");
            var objCardHide = element.querySelector(".player__card");
            var objLabelHide = element.querySelector(".player__label");
            var objImgHide = element.querySelector(".player__img");
            objCardHide.style.display = "none";
            objCardHide.style.opacity = "0";
            objLabelHide.style.opacity = "1";
            objImgHide.style.transform = "translateY(0px)";
          }
          container.classList.add("active");
          objCard.classList.add("active");
          objCard.style.display = "block";
          objCard.style.opacity = "1";
          objLabel.style.opacity = "0";        
          objImg.style.transform = "translateY(-150px)";        
        }		
      });
    });
  
  });
  
  //* ===================== é
  var wc_team = wc_team || {};
  
  wc_team.pitch = function() {
  
    var field = function() {
  
        // Pitch outer bounds
        path.call(this, {
          move: [100, 20],
          lines: [
            [100, 20],
            [20, 560],
            [560, 560],
            [460, 20]
          ]
        });
  
        var grd = this.createLinearGradient(0, 0, 0, 400);
        grd.addColorStop(0.1, '#238C27');
        grd.addColorStop(1, "#2CC932");
        this.fillStyle = grd;
        this.fill();
        this.strokeStyle = "black";
        this.lineWidth = "5";
        this.stroke();
      },
  
      markings = function() {
  
        // Pitch Outline
        path.call(this, {
          move: [110, 30],
          lines: [
            [30, 550],
            [550, 550],
            [450, 30]
          ],
          style: ["white", "3"]
        });
  
        //  Half way line
        path.call(this, {
          move: [76, 260],
          lines: [
            [495, 260]
          ],
          style: ["white", "3"]
        });
  
        // Center circle    
        this.beginPath();
        this.arc(280, 267, 75, 30, 0, true);
        this.strokeStyle = "white";
        this.stroke();
  
        // Away goal
        path.call(this, {
          move: [130, 550],
          lines: [
            [145, 440],
            [435, 440],
            [450, 550]
          ],
          style: ["white", "3"]
        });
  
        // Penalty arc
        this.beginPath();
        this.arc(285, 463, 75, 1.1 * Math.PI, 1.9 * Math.PI, false);
        this.closePath();
        this.strokeStyle = "white";
        this.stroke();
  
        // 6 yard box
        path.call(this, {
          move: [210, 550],
          lines: [
            [215, 500],
            [365, 500],
            [370, 550]
          ],
          style: ["white", "3"]
        });
  
        // Home goal
        path.call(this, {
          move: [175, 30],
          lines: [
            [165, 100],
            [400, 100],
            [390, 30]
          ],
          style: ["white", "3"]
        });
  
        // Penalty arc
        this.beginPath();
        this.arc(285, 81, 60, -1.1 * Math.PI, -1.9 * Math.PI, true);
        this.strokeStyle = "white";
        this.stroke();
  
        // 6 Yard box
        path.call(this, {
          move: [233, 30],
          lines: [
            [230, 60],
            [343, 60],
            [340, 30]
          ],
          style: ["white", "3"]
        });
      }
  
    path = function() {
  
        this.beginPath();
  
        move.call(this, arguments[0].move);
        lines.call(this, arguments[0].lines);
  
        this.closePath();
  
        if (arguments[0].style !== undefined) {
          attr.call(this, arguments[0].style);
        }
      },
  
      move = function() {
        var args = arguments[0];
        this.moveTo(args[0], args[1]);
      },
  
      attr = function() {
        var args = arguments[0];
        this.strokeStyle = args[0];
        this.lineWidth = args[1];
        this.stroke();
      }
  
    lines = function() {
  
      var that = this,
        args = arguments[0];
  
      for (var i = 0; i < args.length; i++) {
        this.lineTo(args[i][0], args[i][1]);
      }
    }
  
    return {
      field: field,
      markings: markings
    }
  }();
  
  wc_team.dragDrap = function() {
  
    var position,
      dragSrc,
  
      // Select new team
      init = function() {
        var players = document.querySelectorAll(".positions ul");
  
        for (var p = 0; p < players.length; p++) {
          players[p].addEventListener("dragstart", dragStart, true);
          players[p].addEventListener("dragend", dragEnd, false);
        }
  
        position = document.querySelectorAll('#starting_11 li');
  
        for (var i = 0; i < position.length; i++) {
          position[i].addEventListener('drop', drop, false);
          position[i].addEventListener('dragenter', cancel, false);
          position[i].addEventListener('dragover', cancel, false);
        }
      },
  
      dragStart = function(e) {
  
        dragSrc = e;
  
        e.dataTransfer.setData("text/html", e.target.outerHTML);
        e.dataTransfer.effectAllowed = "copy";
        e.dataTransfer.dropEffect = "copy";
  
        // Limit droppable player to there positions on pitch
        for (var i = 0; i < position.length; i++) {
          if (e.currentTarget.dataset.pos === position[i].dataset.pos) {
            var id = position[i].id;
            document.getElementById(id).classList.add("highlight");
          }
        }
      },
  
      dragStartOver = function(e) {
  
        dragSrc = e;
  
        console.log(e);
  
        e.dataTransfer.setData("text/html", this.innerHTML);
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.dropEffect = "move";
  
        // Limit droppable player to there positions on pitch
        for (var i = 0; i < position.length; i++) {
          if (e.currentTarget.dataset.pos === position[i].dataset.pos) {
            var id = position[i].id;
            document.getElementById(id).classList.add("highlight");
          }
        }
      },
  
      drop = function(e) {
        cancel(e);
  
        var data = e.dataTransfer.getData("text/html"),
          target = e.currentTarget;
  
        // reenable drag for outgoing player
        if (target.innerHTML !== "") {
          dragReset(target.lastChild.dataset.player);
        }
  
        if (dragSrc.srcElement.parentNode.id === 'starting_11') {
          // Reorder player      
          var dragSrcClass = dragSrc.target.className,
            targetClass = target.className;
  
          dragSrc.target.innerHTML = this.innerHTML;
          dragSrc.target.className = targetClass;
  
          target.innerHTML = data;
          target.className = dragSrcClass;
  
          console.log(dragSrc, target);
        } else {
          // Set new player data
          target.innerHTML = '<a class="remove"></a>' + data;
          document.getElementById(target.id).classList.add('selected');
  
          // Disable draggale property to stop duplicates
          dragSrc.target.draggable = false;
          target.lastChild.setAttribute('draggable', 'false');
        }
  
        dragEnd();
        target.addEventListener("dragstart", dragStartOver, false);
      },
  
      dragEnd = function() {
        for (var i = 0; i < position.length; i++) {
          var id = position[i].id;
          document.getElementById(id).classList.remove('highlight');
        }
      },
  
      cancel = function(e) {
  
        if (e.preventDefault) {
          e.preventDefault();
        }
  
        if (e.stopPropagation) {
          e.stopPropagation();
        }
  
        return false;
      },
  
      // reset players draggable attr
      dragReset = function(name) {
  
        var player = document.querySelector('.positions div[data-player="' + name + '"]');
  
        player.draggable = true;
      }
  
    return {
      init: init
    }
  }();
  
  wc_team.init = function() {
    //Save common elements
    var c = document.getElementById("pitch"),
      ctx = c.getContext("2d");
  
    wc_team.pitch.field.call(ctx);
    wc_team.pitch.markings.call(ctx);
  
    wc_team.dragDrap.init();
  }
  
  // Create the pitch
  wc_team.init();