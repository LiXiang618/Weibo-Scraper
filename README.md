# Weibo-Scraper
Although I am not the original author of the code, I made great contribution on its improvement while working as research assistant at school. For the convenience of its further improvement, I upload it onto Github.

## The following README document was created by two students from Lehigh University, Baiyu and Yin. I think it is a good start point to run the program.

### 1. Purpose:
    This programing is used to web-scraping the data for a specific account by using it's own weibo id.

### 2. How To Get Cookie:
    This program will use the cookie to get access to programmer's weibo account and start the web-scraping process of the target account. In order to do that, we need to get our cookie first.
    a) First download a chrome browser if you do not have one, then go to https://passport.weibo.cn/signin/login.
    b) Open the chrome developer tools.
    c) Click the "newwork" tab and then select the "Preserve log"
    d) Enter your account name and password and log into your account.
    e) Find the "m.weibo.cn" item which listed in the developer tools and then find the "Cookie" under "Request Cookie".
    f) Copy and paste the cookie into the cookie field under weibo class in the program. 
    
### 3. Input File:
    The program will take "Chinese_CSA_farms.xlsx" file as input. It will read in the 5th column which MUST be weibo id as input and store them as the target id list and perform web-scraping on each one of those.
    NOTE: The entire 5th column has to be in Number form in Excel(no scientific or any other form) and Account id ONLY. If this personal does not have a weibo, just leave it blank
    
### 4. How To get Weibo Account ID:
    a) Normal case:
        Typically if a account web address is similary to http://weibo.com/u/5223347681?refer_flag=1001030201_, the account id will be just 5223347681 and shown in the web address
    b) Other case):
        If the we address is similary to http://weibo.com/zhuhainongfushiji?refer_flag=1001030201_ then you need more step to get the Account ID
        b.1) Go to this this web address
        b.2) On the left hand side and under the Follow/Followers/Weibo and find the info area.
        b.3) Click the "查看更多" or "view more" button
        6.4) The web address will become something like http://weibo.com/p/1005052767307765/info?mod=pedit_more and the account id will be just 1005052767307765

    NOTE: Since the program is collect data through the mobile version weibo page, it will ONLY work for the 10 digits account IDs.

### 5. Program:
    The main program will read in the input file and then create a weibo object for every user and call start() function. (The "filter" in the main program is to change the type the post, 0 for all post and 1 for original posts.)
    start(): perform all data collection and output function in there.
    getUserFollowing(): get the id for the people who follow by the target account.
    getUserFollower(): get the id for the people who following the target account.(Fans)
    getUserName(): get user name for target account.
    getUserInfo(): get all user level information.
    getWeiboInfo(): get information for each post. 
    writeCsv(): write the output file.
    
### 6. Output file:
    The program will output csv files. One named "user_info.csv" which has all user level info and one named "xxxxxx.csv" (xx should be account id) for each account has all posts information
    a) user_info.csv
        Username: User name for target account.
        Account ID: Account ID for target account.
        Num of Post:    Total number of posts.
        Num of followers:   Total number of account followed by target account.
        Num of fans:    Total number of account who follow the target account.
        Followers ID:   All account id of account followed by target account.
        Fans ID:    All account id of account who follow the target account.
        
        NOTE: we ONLY collect the number only account id in this case.
    
    b) xxxxxxxx.csv
        Num:    Number id for each post.
        Post:   Full length of content.
        Date:   Date of post
        Like:   Number of like for this post
        Like_ID:    All account id for people who like the post.
        Share:  Number of share for this post
        Share_ID:   all account id for people who share the post.
        Share_Content:  the content fot people share with the post (Separate by $)
        Comment:    Number of comment for this post
        Comment_ID: all account id for people who comment the post.
        Comment_Content:    the content fot people comment on the post (Separate by $)
        
        NOTE: we ONLY collect the number only account id in this case.
    