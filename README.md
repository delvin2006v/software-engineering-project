# soft-engg-project-jan-2025-se-Jan-37
This repository consists of the project work of Team 37 for the Software Engineering Project in Jan-2025. We as a team of 7 collaboratively design and develop an AI agent for IITM Seek Portal to help the students with their course related queries.

### Team Members
1. Ananya Gupta
2. Delvin
3. Kanishk
4. Kishar Kr Nath
5. Shridhar Kumar
7. Soumya Kushwaha
8. Sivasurya E

### GitHub Essentials (*atleast for this project repo*)

#### Getting Started

1. Clone the repository

	```shell
	git clone https://github.com/Delvin-V/soft-engg-project-jan-2025-se-Jan-37.git
	```

	> Note:
	> - The above command clones the repository into your local system.
	> - After that you will be left with the main (default) branch in the local system.

2. Checkout to a branch

	```shell
	git switch -c <local-branch> origin/<remote-branch>
	```

	> Note:
	> - The above command creates a local branch `<local-branch>` and set it to track `origin/<remote-branch>`.
	> - You are also switched to the `<local-branch>`

	```shell
	git pull
	```

	> Note:
	> - The above command pulls the latest updates from the remote branch to your local branch.
	
	- If you want to switch to another existing local branch

	```shell
	git switch <local-branch>
	```
3. Add files/modifications for commit
	- Let's say that you have made some changes to a file and you want to commit to the local branch.

	```shell
	git status
	```

	> Note:
	> - The above command returns the status details of the local directory.
	> - It shows untracked files, modifications, yet-to-commit, merge-conflicts, sync status with the remote branch and many more.
	> - You can use this command to verify before and after commits and pushes.

	- Once you have gone through the above command's output you can decide on which modifications to be commited to the local branch

	```shell
	git add <file-name>, ..
	# or
	git add .
	```

	> Note:
	> - In the first command the changes that are made only in the specified `<file-name>` will be stagged (kept ready) for commit
	> - The second command adds all the modifications for the commit.

4. Making a commit
	- The modifications that were added in the above command will only be committed.

	```shell
	git commit
	```

	> Note:
	> - While executing the above command a file will be opened in the text editor.
	> - There in the first line you can write in brief about the commit.
	> - After leaving a newline inbetween you can write the description of the commit (if needed).
	> - Following that there are a lot of comments in that file please ignore them and save the file to complete the commit.

    - Eg: the file that will be provided
	
	```shell
	Backend Setup

	- Created Flask app, FlaskApi, Init Database 

	# some comments 
	# with info that
	# can be
	# ignored
	```
	- To get the details of all the commits (made by you and others)
	
	```shell
	git log
	```

5. Pushing to the Remote Branch
	```shell
	git push
	```
	> Note:
	> - The above command pushes our commit to the remote branch.
	> - Now the remote repo is updated with the commit.

#### Some Practices

- Since we are working as a team and its important atleast for those who are working on same the same branch to be in sync with others
- Here are some ways to do that

1. Sync with the remote-branch
	- Let's say you and another guy are working on the same branch then,
	- Case 1: If you want to commit your changes and then get in sync with the other
		```shell
		git status # to check for uncommitted modifications
		git commit # make sure that you have nothing left uncommited in order to get sync
		git fetch # fetch the changes from the remote-branch
		git status # see the changes in the remote-branch
		git log # to see all the commits pushed to the remote-branch by both
		git pull # if you are ok with the changes in the remote-branch then pull
		```
		- Now you are in sync with the co-worker (your local system has been updated with the changes made by the other guy)

	- Case 2: You have been working on something and its yet to be completed then, if you want to be in sync with the other
		```shell
		git stash # temporarily save the uncommitted changes, your changes will be removed temporarily
		git pull
		git stash pop # reapply your uncommitted changes
		```
		- Now you uncommitted changes will remain uncommitted but yet you got the latest update from the remote-branch
	- The above procedure can be done before starting to work everyday to ensure sync with the other guy's changes.

2. Sync with the main branch
	- Let's say that we have two branches additional to main.
	- One branch has been merged to the main while the other is not, then
	- Its important for the yet-to-be-merged branch to get the latest update from the main before **merging to the main** to avoid merge conflicts.
	- We have a way,
	```shell
	# as usual ensure that no uncommited changes are left/ everything is stashed
	git fetch origin main # gets the latest changes from main branch
	git status
	git log 
	git pull origin main # pull and apply the latest changes to the <local-branch>
	# Note that the latest changes are brought only to the local-branch not to the remote-branch
	git push # push the latest changes to the remote-branch also
	```
	- Note: The above sync-with-main is **only needed when the remote-branch is ready to be merged with the main.**

3. Merging with main
	- Once a feature is tested and merged with the main branch through a pull request. where the code review is done and discussion about the code is done before merging to the main.
	- After merging the branch can be deleted. A new branch can be created for a new feature to work with.
	```shell
	git branch -d <local-branch>
	```
	> Note:
	> - The above command deletes the local branch.

							Please forgive me for this such long document
