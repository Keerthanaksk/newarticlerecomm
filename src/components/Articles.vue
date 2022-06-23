<template>
    

    <div class="container">
    <h1 v-if="this.topic" class="display-5 m-3">{{this.topic}}</h1>
        <div class="d-grid gap-5 articles p-3 pb-5" v-if="this.topic">
            <Article
                v-for="(article, key) in filteredArticles"
                :key="key"
                :link="article.link"
                :title="article.title"
                :summary="article.summary"
                :clicked="article.clicked"
                :liked="article.liked"
            />
        </div>
        
    </div>

</template>

<script>

    import Article from './Article.vue'

    export default {
        name: 'Articles',
        
        props: {
            topic: String
        },

        components: { Article },

        computed: {
            filteredArticles() {
                const asArray = this.articles.filter(article => article.topic == this.topic)
                
                return asArray
            }
        },
        
        data() {
            return {

                articles: [
                    {
                        link: `https://www.wbcsd.org/Overview/News-Insights/WBCSD-insights/Solving-human-and-societal-challenges-the-real-drivers-behind-innovation`,
                        topic: 'Machine Learning and AI Ethics',
                        title: `Solving human and societal challenges the real drivers behind innovation`,
                        summary: ` The pace of technology innovation is growing ever faster, and we are starting to see wider adoption and applications for emerging technologies such as artificial intelligence (AI) and quantum computing . Fujitsu developed the world's #1 supercomputer, Fugaku, jointly developed with RIKEN, and is also leading with our digital annealing service .`,
                        clicked: 1,
                        liked: 1
                    },
                    {
                        link: `https://www.newswise.com/articles/can-university-of-oklahoma-research-team-clear-up-biases-in-artificial-intelligence`,
                        topic: 'Machine Learning and AI Ethics',
                        title: `Can University of Oklahoma Research Team Clear Up Biases in Artificial Intelligence?`,
                        summary: ` Amy McGovern, Ph.D., leads the National Science Foundation AI Institute for Research on Trustworthy AI in Weather, Climate, and Coastal Oceanography at the University of Oklahoma . McGovern and researchers from Colorado and Washington have noticed grave disparities in AI, noting that the methods are not objective, especially when it comes to geodiversity .`,
                        clicked: 1,
                        liked: 1
                    },
                    {
                        link: `https://www.nature.com/articles/d41586-020-03611-8`,
                        topic: 'Machine Learning and AI Ethics',
                        title: `Prestigious AI meeting takes steps to improve ethics of research`,
                        summary: ` For the first time, the organizers of NeurIPS required speakers to consider the societal impact of their work . The conference required presenters to submit a statement on the broader impact their research could have on society, including any possible negative effects . The organizers also appointed a panel of reviewers to scrutinize papers that raised ethical concerns-- a process that could lead to their rejection .`,
                        clicked: 1,
                        liked: 1
                    },
                    {
                        link: `https://finance.yahoo.com/news/gastroesophageal-reflux-disease-devices-market-144000296.html`,
                        topic: 'Finance and Business',
                        title: `Gastroesophageal Reflu,x Disease Devices Market Research Report by Product Type, Procedure Type, Device Type, Surgery Type, Route of Administration, Dosage Form, End-User, Region - Global  Forecast to 2`,
                        summary: ` The Gastroesophageal Reflux Disease Devices Market size was estimated at USD 4,550.91 million in 2021 and expected to reach USD 5,159.83 million in 2022 . The market is projected to grow at a CAGR 13.55% to reach $9,758.51 million by 2027 . The report provides market sizing and forecast across five major currencies - USD, EUR, JPY, GBP, AUD, CAD, and CHF . It helps organization leaders make better decisions when currency exchange data is readily available .`,
                        clicked: 1,
                        liked: 0
                    },
                    {
                        link: `https://www.investopedia.com/ask/answers/155.asp`,
                        topic: 'Finance and Business',
                        title: `How the News Affects Stock Prices`,
                        summary: ` The relationship between supply and demand is highly sensitive to the news of the moment . But chasing the news is not a good stock-picking strategy for the individual investor . Professional traders react in anticipation of an event, not when the event is reported . Good news will normally cause individuals to buy stocks, an announcement of a new product, a corporate acquisition, and positive economic indicators all translate into buying pressure .`,
                        clicked: 1,
                        liked: 1
                    },
                    {
                        link: `https://www.fdic.gov/news/financial-institution-letters/index.html`,
                        topic: 'Finance and Business',
                        title: `Financial Institution Letters`,
                        summary: ` Financial Institution Letters (FILs) are addressed to the Chief Executive Officers of the financial institutions on the FIL's distribution list . FILs may announce new regulations and policies, new FDIC publications, and a variety of other matters of principal interest to those responsible for operating a bank or savings association .`,
                        clicked: 0,
                        liked: 0
                    },
                    {
                        link: `https://www.postregister.com/news/inl/study-casts-doubt-on-small-modular-reactors-clean-energy-claims/article_0e7cc803-3695-5300-83b0-369ed6e92925.html`,
                        topic: 'Power and Energy',
                        title: `Study casts doubt on small modular reactors' clean-energy claims`,
                        summary: ` US Virgin Islands United States Minor Outlying Islands . United States minor outlying Islands Canada Mexico, United Mexican States Mexico . U.S. Virgin Islands and U.N. territories include Canada, United States of America, U.K. and the United States Virgin Islands . The United States is one of the smallest countries in the world .`,
                        clicked: 1,
                        liked: 1
                    },
                    {
                        link: `https://www.eenews.net/articles/europes-clean-energy-plan-has-a-mining-problem/`,
                        topic: 'Power and Energy',
                        title: `Europe's clean energy plan has a mining problem`,
                        summary: ` Europe's plan to slash Russian fossil fuel imports and accelerate renewable energy production will test its ability to mine or import the materials that are needed for clean energy technology, like copper, lithium and cobalt . It comes as supply chains strain against rising demand for renewable energy globally .`,
                        clicked: 0,
                        liked: 0
                    },
                    {
                        link: `https://www.business-standard.com/article/economy-policy/commercial-entities-reduce-electricity-bills-by-renewable-energy-mercom-122060600332_1.html`,
                        topic: 'Power and Energy',
                        title: `Commercial entities reduce electricity bills by renewable energy: Mercom`,
                        summary: ` The 'C&I Clean Energy Meet 2022' held in Bengaluru witnessed participation from players operating in solar, IT, automobile, manufacturing, chemical, textiles and FMCG sectors . Over 100 players joined the one-day event to discuss opportunities in the domestic sector .`,
                        clicked: 0,
                        liked: 0
                    },
                    {
                        link: `https://fortune.com/2022/06/07/cfos-crypto-large-companies-2024/`,
                        topic: 'Blockchain',
                        title: `CFOs can't avoid crypto-- and 20% of large companies will use it in some way by 2024`,
                        summary: ` Apple may finally be ordered to make chargers just like everyone else . Apple may have been ordered to produce chargers for the first time ever . Apple's iPhone and iPad line-in-the-line chargers can be used to charge the next generation of iPhones and iPads .`,
                        clicked: 0,
                        liked: 0
                    },
                    {
                        link: `https://www.cnbc.com/2022/02/08/-research-shows-cryptocurrency-adoption-among-hispanics-is-high.html`,
                        topic: 'Blockchain',
                        title: `Why U.S. minority communities may turn to cryptocurrencies to pay their bills`,
                        summary: ` A recent survey found that while 69% of all U.S. adults are white, only 62% of cryptocurrency owners are white . Asian, Black and Hispanic adults are more likely than white adults to have invested in, traded or used cryptocurrency . One reason may be that cryptocurrency is booming in Latin America, particularly in countries like Argentina and Mexico .`,
                        clicked: 1,
                        liked: 1
                    },
                    {
                        link: `https://cryptopotato.com/australian-mayor-proposes-paying-taxes-in-cryptocurrency/`,
                        topic: 'Blockchain',
                        title: `Australian Mayor Proposes Paying Taxes in Cryptocurrency`,
                        summary: ` Mayor of Gold Coast, Australia, has suggested that Australians could pay their local property taxes in cryptocurrency . Gold Coast Mayor Tom Tate sees crypto payments as a way to communicate Australia's innovative virtue, effectively attracting young people . He also noted that the council will recruit a chief investment officer tasked with promoting "innovation," and looking into "joint ventures" involving the council's land .`,
                        clicked: 0,
                        liked: 0
                    },
                    {
                        link: `https://www.space.com/uranus-haze-neptune-layers-different-colors`,
                        topic: 'Space News Research',
                        title: `Shades of Uranus: Scientists know why the planet and Neptune are different hues of blue`,
                        summary: ` A new study shows that a "stagnant, sluggish" atmosphere on Uranus allows haze to build up and concentrate on the gas giant, making it a "whiter" cyan blue than Neptune's cerulean blue . It is the first study to take into account wavelengths from ultraviolet to near-infrared, rather than concentrating on a handful of light waves .`,
                        clicked: 1,
                        liked: 1
                    },
                    {
                        link: `https://www.indiatoday.in/education-today/news/story/iit-madras-creates-research-group-to-manufacture-in-outer-space-1947259-2022-05-09`,
                        topic: 'Space News Research',
                        title: `IIT Madras creates research group to manufacture in outer space`,
                        summary: ` IIT Madras has established a research group to develop technology for manufacturing products in outer space or extraterrestrial places . India is a global leader in the development and application of technologies for launch vehicles and satellites . The Extra-Terrestrial Manufacturing (ExTem) research group will work on the first ever Microgravity Drop Tower Research Facility in India .`,
                        clicked: 1,
                        liked: 1
                    },
                    {
                        link: `https://news.satnews.com/2022/06/05/eos-space-systems-joins-smartsat-crc-as-a-core-partner-for-the-development-of-optical-comms-compact-rf-tactical-terminals/`,
                        topic: 'Space News Research',
                        title: `EOS Space Systems joins SmartSat CRC as a core partner for the development of optical comms + compact RF tactical terminals SatNews`,
                        summary: ` EOS Space Systems has become a core partner for the SmartSat Co-operative Research Centre, becoming the 20th core partner alongside leading universities and global corporations . Project CHORUS aims to build on existing Australian technology in compact RF tactical terminals and optical communication to develop "leap-frogging" technology that exploits bearer diversity .`,
                        clicked: 1,
                        liked: 0
                    }
                ]

            }
        }
    }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    
    .articles {
        max-height: 70vh;
        overflow-y: scroll;
    }

</style>







