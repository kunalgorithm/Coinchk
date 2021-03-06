/**
 * Our Vue.js application.
 *
 * This manages the entire front-end website.
 */

// The API we're using for grabbing metadata about each cryptocurrency
// (including logo images). The service can be found at:
// https://www.cryptocompare.com/api/
let CRYPTOCOMPARE_API_URI = "https://min-api.cryptocompare.com";
let CRYPTOCOMPARE_URI = "https://www.cryptocompare.com";

// The API we're using for grabbing cryptocurrency prices.  The service can be
// found at: https://coinmarketcap.com/api/
let COINMARKETCAP_API_URI = "https://api.coinmarketcap.com";

let CHECK_MARK = "https://thetinylife.com/wp-content/uploads/2017/08/checked-checkbox-512.png";
let WRONG_MARK = "https://cdn-images-1.medium.com/max/1600/1*-ioz6cNvcD9roazfd6TzGg.png";

let LOCAL_API = "http://localhost:8000/coins?from=1&to=100";
let SERVER_API = "http://104.131.19.132:8000/coins/?from=1&to=20";

// Designate the local or server api here
let COINCHK_API = SERVER_API

// The amount of milliseconds (ms) after which we should update our currency
// charts.
let UPDATE_INTERVAL = 60 * 1000;

let app = new Vue({
  el: "#app",
  delimiters: ['[[', ']]'],
  data: {
    coins: [],
    coinData: {},
    parseData: {},
    openSource: 0

  },
  methods: {

    /**
     * Load up all cryptocurrency data.  This data is used to find what logos
     * each currency has, so we can display things in a friendly way.
     */
    getCoinData: function() {
      let self = this;

      axios.get(CRYPTOCOMPARE_API_URI + "/data/all/coinlist")
        .then((resp) => {
          this.coinData = resp.data.Data;
          this.getCoins();
        })
        .catch((err) => {
          this.getCoins();
          console.error(err);
        });
    },

    /**
     * Get the top 10 cryptocurrencies by value.  This data is refreshed each 5
     * minutes by the backing API service.
     */
    getCoins: function() {
      let self = this;

      axios.get(COINMARKETCAP_API_URI + "/v1/ticker/?limit=100")
        .then((resp) => {
          this.coins = resp.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },

    /**
     * Given a cryptocurrency ticket symbol, return the currency's logo
     * image.
     */
    getCoinImage: function(symbol) {

      // These two symbols don't match up across API services. I'm manually
      // replacing these here so I can find the correct image for the currency.
      //
      // In the future, it would be nice to find a more generic way of searching
      // for currency images
      symbol = (symbol === "MIOTA" ? "IOT" : symbol);
      symbol = (symbol === "VERI" ? "VRM" : symbol);
      try {
        return CRYPTOCOMPARE_URI + this.coinData[symbol].ImageUrl
      }
      catch(err) {
        return CRYPTOCOMPARE_URI + this.coinData["BTC"].ImageUrl
      }

      // return CRYPTOCOMPARE_URI + this.coinData[symbol].ImageUrl ? CRYPTOCOMPARE_URI + this.coinData[symbol].ImageUrl : CRYPTOCOMPARE_URI + this.coinData["BTC"].ImageUrl ;
      // return CRYPTOCOMPARE_URI + this.coinData["BTC"].ImageUrl;
    },

    // DEV METHODS
    getParseData: function() {
      let self = this;
      // const proxyurl = "https://cors-anywhere.herokuapp.com/";
      // const url = "http://coinchk.com/parsedData.json"; // site that doesn’t send Access-Control-*
      // fetch(proxyurl + url) // https://cors-anywhere.herokuapp.com/https://example.com
      // .then(response => response.text())
      // // .then(contents => console.log(contents))
      // .then((resp) => {
      //     this.parseData = resp.data;
      //   })
      // .catch(() => console.log("Can’t access " + url + " response. Blocked by browser?"))

      axios.get(COINCHK_API)
        .then((resp) => {
          // console.log(resp.data);
          this.parseData = resp.data;
        })
        .catch((err) => {
          console.error(err);
        });
      
    },
    getOpenSource: function(num) {
      this.openSource = this.parseData[parseInt(num)]["is_open_sourced"]
      return this.openSource ? CHECK_MARK : WRONG_MARK;
      
    },
    
    getForked: function(num) {
      return (this.parseData[parseInt(num)]["is_forked"] && this.openSource) ? WRONG_MARK : CHECK_MARK;
    },
    getReadme: function(num) {
      return (this.parseData[parseInt(num)]["is_readme_good"] && this.openSource) ? CHECK_MARK : WRONG_MARK;
    },
    getContributions: function(num) {
      return (this.parseData[parseInt(num)]["is_contributor_active"] && this.openSource) ? CHECK_MARK : WRONG_MARK;
    },
    getRecentCommits: function(num) {
      return (this.parseData[parseInt(num)]["is_development_recent"] && this.openSource) ? CHECK_MARK : WRONG_MARK;
    },
    getIssues: function(num) {
      return (this.parseData[parseInt(num)]["is_open_issues_small"] && this.openSource) ? CHECK_MARK : WRONG_MARK;
    },
    getStars: function(num) {
      return this.parseData[parseInt(num)]["num_stars"];
    },
    getScore: function(num) {
      return this.parseData[parseInt(num)]["dev_score"];
    },

    // END DEV METHODS

    /**
     * Return a CSS color (either red or green) depending on whether or
     * not the value passed in is negative or positive.
     */
    getColor: (num) => {
      return num > 0 ? "color:green;" : "color:red;";
    },
  },

  /**
   * Using this lifecycle hook, we'll populate all of the cryptocurrency data as
   * soon as the page is loaded a single time.
   */
  created: function () {
    this.getCoinData();
    this.getParseData();
  }
});

/**
 * Once the page has been loaded and all of our app stuff is working, we'll
 * start polling for new cryptocurrency data every minute.
 *
 * This is sufficiently dynamic because the API's we're relying on are updating
 * their prices every 5 minutes, so checking every minute is sufficient.
 */
setInterval(() => {
  app.getCoins();
}, UPDATE_INTERVAL);




