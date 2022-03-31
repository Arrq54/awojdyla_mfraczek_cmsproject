<script>
    import {Router, Link} from "svelte-navigator";
    window.onload = function () {
      fetch("test")
        .then((response) => response.json())
        .then((data) => console.log(data));
    };

    let navbarItems = [
        "Features",
        "Pricing",
        "FAQs",
        "About"
    ]

    let slider = {
        src: "../../images/sliderPlaceholder.png",
        labels: ["First side label", "Second side label", "Third side label"]
    }

    let actualSliderSide = 0;

    function changeSliderSide(x){
        if(actualSliderSide==0 && x==-1){
            actualSliderSide = 2
        }else if(actualSliderSide==2 && x==1){
            actualSliderSide = 0
        }else{
            actualSliderSide += x
        }
    }
  </script>
<style>
    .navbar-item{
        margin: 5px 20px;
    }
    .navbar{
        padding-left: 20%;
        margin-bottom: 10px;
    }
    .flex{
        display: flex
    }
    .slider{
        width: 100%;
        height: 500px;
        position: relative;
    }
    .arrow{
        width: 20px;
        height: 100px;
        position: absolute;
        top: 50%;
        cursor: pointer;
        transition: 0.5s all ease;
    }
    .arrow:hover{
        transition: 0.5s all ease;
        transform: translateY(-10px);
    }
    .arrow-left{
        left: 5%;
    }
    .arrow-right{
        right: 5%;
    }
    .slider-label{
        position: absolute;
        bottom: 20px;
        left: calc(50% - 50px);
    }
</style>
<div class="main">
    <!--NAVBAR MENU-->
    <div class="navbar flex">
        <div class="navbar-item">
            Icon
        </div>
        <Router>
            {#each navbarItems as item}
                <div class="navbar-item"><Link to={item}>{item}</Link></div>
            {/each}
        </Router>
    </div>
    <!--SLIDER-->
    <div class="slider" style="background-image: url({slider.src});">
        <div class="arrow arrow-left" on:click={()=>changeSliderSide(-1)}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M224 480c-8.188 0-16.38-3.125-22.62-9.375l-192-192c-12.5-12.5-12.5-32.75 0-45.25l192-192c12.5-12.5 32.75-12.5 45.25 0s12.5 32.75 0 45.25L77.25 256l169.4 169.4c12.5 12.5 12.5 32.75 0 45.25C240.4 476.9 232.2 480 224 480z"/></svg>
        </div>
        <div class="arrow arrow-right" on:click={()=>changeSliderSide(1)}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M96 480c-8.188 0-16.38-3.125-22.62-9.375c-12.5-12.5-12.5-32.75 0-45.25L242.8 256L73.38 86.63c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0l192 192c12.5 12.5 12.5 32.75 0 45.25l-192 192C112.4 476.9 104.2 480 96 480z"/></svg>
        </div>
        <div class="slider-label">
            <h4>{slider.labels[actualSliderSide]}</h4>
        </div>
    </div>
</div>