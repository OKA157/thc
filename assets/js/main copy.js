var main;
var propsList = [];

document.addEventListener('DOMContentLoaded',async () => {
  const main = document.getElementById("main");
  const home = document.getElementById("home");
  const create = document.getElementById("create");
  const active = document.getElementById("active");
  const closed = document.getElementById("closed");

  const homeContents = document.getElementById("homeContents");
  const createContents = document.getElementById("createContents");
  const activeContents = document.getElementById("activeContents");
  const closedContents = document.getElementById("closedContents");

  homeContents.style.display = 'block';
  createContents.style.display = 'none';
  activeContents.style.display = 'none';
  closedContents.style.display = 'none';

  home.addEventListener('click', function(event) {
      event.preventDefault();
      homeContents.style.display = 'block';
      createContents.style.display = 'none';
      activeContents.style.display = 'none';
      closedContents.style.display = 'none';
  });

  create.addEventListener('click', function(event) {
      event.preventDefault();
      homeContents.style.display = 'none';
      createContents.style.display = 'block';
      activeContents.style.display = 'none';
      closedContents.style.display = 'none';
  });

  active.addEventListener('click', async function(event) {
      event.preventDefault();
      var activeVotes = await getActiveData();
      homeContents.style.display = 'none';
      createContents.style.display = 'none';
      activeContents.style.display = 'block';
      closedContents.style.display = 'none';
      document.getElementById("activeContainer").innerHTML = "";
      for(var x=0;x<activeVotes.length; x++)
      {
        await addItemList("activeContainer", activeVotes[x], "Active");
      }
  });

  closed.addEventListener('click', async function(event) {
      event.preventDefault();
      var closedVotes = await getClosedData();
      homeContents.style.display = 'none';
      createContents.style.display = 'none';
      activeContents.style.display = 'none';
      closedContents.style.display = 'block';
      document.getElementById("closedContainer").innerHTML = "";
      for(var x=0;x<closedVotes.length; x++)
      {
        await addItemList("closedContainer", closedVotes[x], "Closed");
      }
      
  });

  var props = 0;
  var propCounter = 0;
  addPropBtn = document.getElementById("addInputProp");
  voteBtn = document.getElementById("voteBtn");
  testingBtn = document.getElementById("testingBtn");
  addPropBtn.addEventListener("click", addProp);
  voteBtn.addEventListener("click", createVoting);
  testingBtn.addEventListener("click", voteExample);
  
  function voteExample() 
  {

    var Title = document.getElementById("title");
    var Expiring = document.getElementById("expDate");
    var Closing = document.getElementById("closeDate");
    var Proposition = document.getElementById("Prop0");

    Title.setAttribute("value","Example Vote");
    Expiring.setAttribute("value","2023-11-23");
    Closing.setAttribute("value","2023-11-07");
    Proposition.setAttribute("value","My 1st proposition.");
  }

  // CREATE A VOTING
  function createVoting() 
  {
    // propCounter
    var Key = generateKey(8);
    var Title = document.getElementById("title").value;
    var Expiring = document.getElementById("expDate").value;
    var Closing = document.getElementById("closeDate").value;
    var Response = document.getElementById("voteResponse");
    var propValues = [];
    for(var i=0; i<propsList.length; i++)
    {
      var propElement = document.getElementById(propsList[i]);
      var propValue = propElement.value;
      propValues.push(propValue);
    }
    const data = {key: Key, title: Title, expiring: Expiring, closing: Closing, props: propValues};
    
    var res = fetch('http://127.0.0.1:8001/submitVote', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'}
    })
    .then(response => 
      {
        if (response.ok) 
        {
          document.getElementById("title").value = null;
          document.getElementById("expDate").value = null;
          document.getElementById("closeDate").value = null;
          propValues = null;
          for(var i=0; i<propsList.length; i++)
          {
            var propElement = document.getElementById(propsList[i]);
            propElement.value = null;
          }
          return response.json();
        } 
        else 
        {
            Response.classList = "text-danger";
            Response.innerHTML = "Request failed";
            throw new Error("Request failed");
        }
      })
    .then(data => 
      {
        Response.classList = "text-success";
        Response.innerHTML=data.message;
        console.log("Success:", data);
      })
    .catch(error => 
      {
        Response.classList = "text-danger";
        Response.innerHTML=data.error;
        console.error("Error:", error);
      });
  }

  // SUBMIT A VOTE
async function confirmVote(id, option) {
  const data = { key: id, option: option };

  try {
      const response = await fetch('http://127.0.0.1:8001/confirmOption', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: { 'Content-Type': 'application/json' }
      });

      if (response.ok) {
          console.log("Vote Submitted Successfully");
          const data = await response.json();
          return data;
      } else {
          throw new Error("Request failed");
      }
  } catch (error) {
      console.error("Error:", error);
      return { error: error.message };
  }
}

  // GET ACTIVE VOTINGS
  async function getActiveData() {
    try {
        // Perform the fetch call and wait for the response
        let response = await fetch('http://127.0.0.1:8001/listActiveVotes', {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error("Request failed");
        }
        let data = await response.json();
        console.log("DATA ACTIVE: ",data);
        return data;

    } catch (error) {
        // Log the error message
        console.error("Error:", error);
    }
  }

  async function getClosedData() {
    try {
        // Perform the fetch call and wait for the response
        let response = await fetch('http://127.0.0.1:8001/listClosedVotes', {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error("Request failed");
        }
        let data = await response.json();
        console.log("DATA: CLOSED",data);
        return data;

    } catch (error) {
        // Log the error message
        console.error("Error:", error);
    }
  }
  
  function decodeData(data) {
    // Function to decode Base64 strings
    function decodeBase64(encodedString) {
        return decodeURIComponent(escape(atob(encodedString)));
    }

    // Function to convert Unix timestamp to Date string
    function convertTimestamp(unixTimestamp) {
        const date = new Date(unixTimestamp * 1000);
        return date.toLocaleString();
    }

    // Create a copy of the data to avoid mutating the original object
    const decodedData = { ...data };

    // Decode the title
    if (decodedData.title) {
        decodedData.title = decodeBase64(decodedData.title);
    }

    // Decode the propositions
    if (decodedData.propositions) {
        decodedData.propositions = JSON.parse(decodedData.propositions[0]).map(prop => decodeBase64(prop));
    }

    // Convert the closing and expiry timestamps
    if (decodedData.closing) {
        decodedData.closing = convertTimestamp(decodedData.closing);
    }
    if (decodedData.expiry) {
        decodedData.expiry = convertTimestamp(decodedData.expiry);
    }

    return decodedData;
}

  function generateKey(length) 
  {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    const charactersLength = characters.length;

    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    return result;
  }

  function addProp()
  {
    // Create a new input element
    var input = document.createElement("input");
    input.type = "text";
    input.id = "Prop"+propCounter;
    propsList.push(input.id);
    input.className = "form-control";
    switch(props){
      case 0:
        input.placeholder = "Yes.";
        break;
      case 1:
        input.placeholder = "No.";
        break;
      case 2:
        input.placeholder = "Maybe.";
        break;
      default:
        input.placeholder = "Propostion.";
        break;
    }    
    input.style = "margin-bottom: 1%; width: 95%; font-style: italic; display: inline-block;";
    // Create a new delete button
    var deleteBtn = document.createElement("span");
    deleteBtn.id = "removeProp"+propCounter;
    deleteBtn.name = "Prop"+propCounter;
    deleteBtn.style = "display: inline-block; height: 100%; width: 4%; color:black; margin-left: 1%; padding: 0 0 0 0;";
    deleteBtn.innerHTML='<button type="button" class="btn-close btn-close" aria-label="Close"></button>';
    deleteBtn.addEventListener("click", function(){
      propsList.splice(propsList.indexOf(input.id),1);
      input.remove();
      props= props-1;
      this.remove();
    });
    // Get the div with the id 'propositions'
    var propositionsDiv = document.getElementById("propositions");
    // Append the input element to the div
    propositionsDiv.appendChild(input);
    if(props != 0)
    {
      propositionsDiv.appendChild(deleteBtn);
    }
    props= props+1;
    propCounter = propCounter+1;
  }

  function addItemList(container, data, type) {
    var closingDate = data.closing;
    var titleText = data.title;
    var expiry = data.expiry;
    var propositions = data.propositions;
    var idKey = data.key;

    // Parse target date from the provided string
    const targetDate = new Date(closingDate.replace(' ', 'T')).getTime();

    // Get container element
    var contDiv = document.getElementById(container);

    // Create countdown container
    var contentDiv = document.createElement("div");
    contentDiv.classList = "countdown-container";
    contDiv.appendChild(contentDiv);

    // Create item container
    var itemList = document.createElement("div");
    itemList.classList = "item-style";
    contentDiv.appendChild(itemList);

    // Title
    var itemTitle = document.createElement("h3");
    itemTitle.classList = "item-font";
    itemTitle.textContent = titleText;
    itemList.appendChild(itemTitle);

    // Additional info container (initially hidden)
    var additionalInfo = document.createElement("div");
    additionalInfo.classList = "additional-info";
    itemList.appendChild(additionalInfo);

    // Dates
    var dates_div = document.createElement("div");
    dates_div.classList = "additional-info-dates";
    additionalInfo.appendChild(dates_div);

    var closing_div = document.createElement("div");
    closing_div.classList = "additional-info-item";
    closing_div.innerHTML = '<b><i class="fa-regular fa-calendar-check"></i><p style="margin-left:6px;">Closing date:</b> ' + closingDate + '</p>';
    dates_div.appendChild(closing_div);

    var exp_div = document.createElement("div");
    exp_div.classList = "additional-info-item";
    exp_div.innerHTML = '<b><i class="fa-solid fa-circle-xmark"></i><p style="margin-left:6px;">Expiry date:</b> ' + expiry + '</p>';
    dates_div.appendChild(exp_div);

    // Propositions
    var options_div = document.createElement("div");
    options_div.classList = "props-container";
    additionalInfo.appendChild(options_div);

    var confirm_div = document.createElement("div");
    confirm_div.classList = "props-container";
    additionalInfo.appendChild(confirm_div);

    var confirmButton = document.createElement("button");
    confirmButton.classList = "confirm-vote-button";
    confirmButton.textContent = "Confirm Vote";
    confirmButton.value = idKey;
    confirm_div.appendChild(confirmButton);

    if (type === "Active") {
        propositions.forEach(function(proposition) {
            var prop_div = document.createElement("div");
            prop_div.classList = "props-item";
            prop_div.innerHTML = '<b>' + proposition + '</b>';
            options_div.appendChild(prop_div);

            prop_div.addEventListener('click', function() {
                // Remove props-item-selected class from all prop_div elements
                var allPropsItems = document.querySelectorAll('.props-item');
                allPropsItems.forEach(function(item) {
                    item.classList.remove('props-item-selected');
                });

                // Add props-item-selected class to the clicked prop_div
                prop_div.classList.add('props-item-selected');

                // Display the confirm button
                confirmButton.style.display = 'block';

                // Store the selected proposition in a data attribute of the confirm button
                confirmButton.dataset.selectedProposition = proposition;
            });
        });

        confirmButton.addEventListener('click', async function() {
          var selectedProposition = confirmButton.dataset.selectedProposition;
          if (selectedProposition) {
              // Hide all props-item elements in the current options_div
              var currentPropsItems = options_div.querySelectorAll('.props-item');
              currentPropsItems.forEach(function(item) {
                  item.style.display = 'none';
              });
      
              confirmButton.style.display = 'none';
              var result = await confirmVote(confirmButton.value, selectedProposition);
              
              var confirmationMessage = document.createElement("h4");
              console.log("REESULT",result.message);

              if (result.message === "Vote Sumbitted Successfully!") {
                  confirmationMessage.classList = "confirmation-message";
                  confirmationMessage.innerHTML = "Vote confirmed for: <b>" + selectedProposition + "</b>";
              } else {
                  confirmationMessage.classList = "error-message";
                  confirmationMessage.innerHTML = "Failed to submit vote. Try again later.";
              }
              confirm_div.appendChild(confirmationMessage);
          }
      });
    }

    if (type === "Closed") {
      propositions.forEach(function(proposition) {
          var prop_div = document.createElement("div");
          prop_div.classList = "props-item-closed";
          prop_div.innerHTML = '<b>' + proposition + '</b>';
          options_div.appendChild(prop_div);
      });
  }

    // Counter
    const countdownElement = document.createElement('div');
    countdownElement.classList = "countdownElement";
    contentDiv.appendChild(countdownElement);

    function updateCountdown() {
        const now = new Date().getTime();
        const timeRemaining = targetDate - now;

        if (timeRemaining < 0) {
            countdownElement.textContent = 'The event has ended!';
            // clearInterval(interval);
            return;
        }

        const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

        countdownElement.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;
    }

    // Update the countdown immediately and then every second
    if (type === "Active") {
      updateCountdown();
      const interval = setInterval(updateCountdown, 1000);
    }
    

    // Toggle function to expand/collapse additional info
    function toggleAdditionalInfo() {
        if (additionalInfo.style.display === 'block') {
            additionalInfo.style.display = 'none';
        } else {
            // Collapse any previously expanded item
            var expandedItems = document.querySelectorAll('.item-style .additional-info');
            expandedItems.forEach(function(item) {
                item.style.display = 'none';
            });
            // Expand clicked item
            additionalInfo.style.display = 'block';
        }
    }

    // Attach click event listener to item title for toggling additional info
    itemTitle.addEventListener('click', toggleAdditionalInfo);
}




});

document.addEventListener('DOMContentLoaded', () => {
  "use strict";

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Sticky Header on Scroll
   */
  const selectHeader = document.querySelector('#header');
  if (selectHeader) {
    let headerOffset = selectHeader.offsetTop;
    let nextElement = selectHeader.nextElementSibling;

    const headerFixed = () => {
      if ((headerOffset - window.scrollY) <= 0) {
        selectHeader.classList.add('sticked');
        if (nextElement) nextElement.classList.add('sticked-header-offset');
      } else {
        selectHeader.classList.remove('sticked');
        if (nextElement) nextElement.classList.remove('sticked-header-offset');
      }
    }
    window.addEventListener('load', headerFixed);
    document.addEventListener('scroll', headerFixed);
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = document.querySelectorAll('#navbar a');

  function navbarlinksActive() {
    navbarlinks.forEach(navbarlink => {

      if (!navbarlink.hash) return;

      let section = document.querySelector(navbarlink.hash);
      if (!section) return;

      let position = window.scrollY + 200;

      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active');
      } else {
        navbarlink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navbarlinksActive);
  document.addEventListener('scroll', navbarlinksActive);

  /**
   * Mobile nav toggle
   */
  const mobileNavShow = document.querySelector('.mobile-nav-show');
  const mobileNavHide = document.querySelector('.mobile-nav-hide');

  document.querySelectorAll('.mobile-nav-toggle').forEach(el => {
    el.addEventListener('click', function(event) {
      event.preventDefault();
      mobileNavToogle();
    })
  });

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavShow.classList.toggle('d-none');
    mobileNavHide.classList.toggle('d-none');
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navbar a').forEach(navbarlink => {

    if (!navbarlink.hash) return;

    let section = document.querySelector(navbarlink.hash);
    if (!section) return;

    navbarlink.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  const navDropdowns = document.querySelectorAll('.navbar .dropdown > a');

  navDropdowns.forEach(el => {
    el.addEventListener('click', function(event) {
      if (document.querySelector('.mobile-nav-active')) {
        event.preventDefault();
        this.classList.toggle('active');
        this.nextElementSibling.classList.toggle('dropdown-active');

        let dropDownIndicator = this.querySelector('.dropdown-indicator');
        dropDownIndicator.classList.toggle('bi-chevron-up');
        dropDownIndicator.classList.toggle('bi-chevron-down');
      }
    })
  });

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector('.scroll-top');
  if (scrollTop) {
    const togglescrollTop = function() {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
    window.addEventListener('load', togglescrollTop);
    document.addEventListener('scroll', togglescrollTop);
    scrollTop.addEventListener('click', window.scrollTo({
      top: 0,
      behavior: 'smooth'
    }));
  }

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Clients Slider
   */
  new Swiper('.clients-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 2,
        spaceBetween: 40
      },
      480: {
        slidesPerView: 3,
        spaceBetween: 60
      },
      640: {
        slidesPerView: 4,
        spaceBetween: 80
      },
      992: {
        slidesPerView: 6,
        spaceBetween: 120
      }
    }
  });

  /**
   * Init swiper slider with 1 slide at once in desktop view
   */
  new Swiper('.slides-1', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    }
  });

  /**
   * Init swiper slider with 3 slides at once in desktop view
   */
  new Swiper('.slides-3', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 40
      },

      1200: {
        slidesPerView: 3,
      }
    }
  });

  /**
   * Porfolio isotope and filter
   */
  let portfolionIsotope = document.querySelector('.portfolio-isotope');

  if (portfolionIsotope) {

    let portfolioFilter = portfolionIsotope.getAttribute('data-portfolio-filter') ? portfolionIsotope.getAttribute('data-portfolio-filter') : '*';
    let portfolioLayout = portfolionIsotope.getAttribute('data-portfolio-layout') ? portfolionIsotope.getAttribute('data-portfolio-layout') : 'masonry';
    let portfolioSort = portfolionIsotope.getAttribute('data-portfolio-sort') ? portfolionIsotope.getAttribute('data-portfolio-sort') : 'original-order';

    window.addEventListener('load', () => {
      let portfolioIsotope = new Isotope(document.querySelector('.portfolio-container'), {
        itemSelector: '.portfolio-item',
        layoutMode: portfolioLayout,
        filter: portfolioFilter,
        sortBy: portfolioSort
      });

      let menuFilters = document.querySelectorAll('.portfolio-isotope .portfolio-flters li');
      menuFilters.forEach(function(el) {
        el.addEventListener('click', function() {
          document.querySelector('.portfolio-isotope .portfolio-flters .filter-active').classList.remove('filter-active');
          this.classList.add('filter-active');
          portfolioIsotope.arrange({
            filter: this.getAttribute('data-filter')
          });
          if (typeof aos_init === 'function') {
            aos_init();
          }
        }, false);
      });

    });

  }

  /**
   * Animation on scroll function and init
   */
  function aos_init() {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', () => {
    aos_init();
  });

});