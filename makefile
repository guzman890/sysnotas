main:
	git commit -a -m "GG"
	git push origin branch3

merge:
	git checkout master
	git merge branch2
	git push