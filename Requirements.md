.

# **Project Spec: The "Gig-ography" Archive & Analytics Engine**

### **1\. Core Objective**

Create the entire project for a personal, public-facing static website hosted on **GitHub Pages** that archives a lifetime of concerts and festivals. The system must automate data collection from Gmail, reconcile it with manual entries, and enrich it with setlist data and media links.

### **2\. Technical Architecture**

* **Frontend:** Simple, responsive React or Vue.js app (Vite-based) styled with **Tailwind CSS**.  
* **Data Storage:** A single master\_gigs.yaml file in the GitHub repository.  
* **Hosting:** GitHub Pages.  
* **Workflow:** Local Python/Node script \\rightarrow Manual Review \\rightarrow Git Push.

### **3\. The "Solicitor" Tool (Local Script)**

This is a CLI tool you run on your machine before pushing to GitHub.

* **Input Mechanism:** \* Takes a .txt file containing raw copy-paste output from **Gemini (Gmail Extension)**.  
  * Reads a manual\_entries.yaml for gigs not found in email.  
* **Conflict Logic:** \* If a gig exists in both, the Solicitor data (from email) **overrides** manual dates/years to ensure accuracy.  
* **Enrichment Engine:**  
  * **Setlist.fm API:** Scrapes specific setlists. If no setlist exists for that date, it calculates an **average setlist** based on the artist's tour that year.  
  * **Image Scraper:** Finds a "live" photo based on Artist \+ Venue \+ Date or the official festival poster.  
  * **Streaming Links:** Fetches **Apple Music** and **Spotify** artist IDs.  
* **Output:** Generates a proposed\_changes.yaml for user verification.

### **4\. UI & Analytics Requirements**

* **The Grid:** Optimized for \~50 entries. Cards display the event image, date, and venue.  
* **Festival Mode:** For festivals, display the lineup poster. The UI must allow a "Who I Saw" selection to highlight specific artists from the lineup.  
* **Analytics Dashboard:**  
  * **Artist Leaderboard:** Ranked by "Gigs Seen" and "Total Songs Heard."  
  * **Global Song Stats:** Most heard song across your entire lifetime of gigs.  
  * **Venue Stats:** Top 5 most-visited venues.  
* **No Social Sharing:** Strictly a personal archive; no "Share to Social" buttons.

### **5\. Data Schema (master\_gigs.yaml)**

`- artist: "Artist Name"`  
  `date: YYYY-MM-DD`  
  `venue: "Venue Name"`  
  `city: "City"`  
  `type: "gig" or "festival"`  
  `setlist_url: "link"`  
  `total_songs: 18`  
  `top_songs: ["Song A", "Song B"]`  
  `image_url: "link"`  
  `streaming:`  
    `spotify: "link"`  
    `apple: "link"`  
