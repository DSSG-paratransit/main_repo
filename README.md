<<<<<<< HEAD
# dssg_paratransit

Use the Access_Analysis_Rproject folder to get the Rproject.

The Rproj has a directory called "R" that contains various scripts for QC'ing and accessing more information contained in the trip data thus far.

Place all relevant data .csv files in the "data" directory to have easy access to it.


#PYTHON SCRIPTS FOLDER:
- given single_day_clean.csv, run add_Time_Windows.py to add relevant pickup and time windows to the file.
- get_URIDs.py will make, from the pandas.data.frame make in add_Time_Windows.py, a list of URID-class objects for all unhandled request id's
- get_busRuns.py will take the data from add_Time_Windows.py and a given bus run number and spit out the remaining relevant route information for the rest of the day AFTER the breakdown time
- get_buses_realtime.ipynb: IPython Notebook that runs through how to use these scripts

=======
### How to create your own team blog starting from this example

For [jekyll](http://jekyllrb.com) to generate the web-pages to be visible through a web-browser, your blog needs to live on the `gh-pages` branch of your repository.

1. **Create a gh-pages branch**: To do this, enter the settings of your repo, launch the automatic page generator (under the "Github pages" heading), and click through to generate the default setting. 

1. **Pull this branch to your local copy of the repo**. To do this you will need to issue the following on the terminal command line: 

        git pull upstream
    	git checkout gh-pages
	    git pull upstream gh-pages

   at which point your directory should contain the auto-generated default content from 
   Github's automatic page generator. We'll soon get rid of that.

1. **Bootstrap your content from this repo**: Delete the auto-generated content in this branch  and copy over the content from this repository. 

1. Edit the following: 
   
   - `about.md`: Describe the project
   - `_config.yml`: Set the configuration variables for your own blog.
   - `_posts`: Use the first post in this repo as a template for creating your own posts.
   
1. **Commit everything**, push it and make your first pull request - you are off! 
   
   *Note*: When you make pull requests, don't forget that you will want to make pull requests against the `gh-pages` branch of your team repo, *not* the `master` branch. Github allows you to select the base repo, and the base branch from a dropdown menu that appears when you ask to make a pull request. 

1. Use branches and pull requests to add more posts and more content to the blog. 

1. Customize! For ideas, inspiration and code, take a look at [http://jekyllthemes.org/](http://jekyllthemes.org/)



 
>>>>>>> fcece44389bfa1040e70facebb4fb3395e74c415
