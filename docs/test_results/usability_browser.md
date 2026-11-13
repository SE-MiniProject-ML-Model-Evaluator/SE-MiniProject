# Usability and cross-browser test results (TC-14, TC-15)

Fill this in while you run the tests. Record what you actually observe, including problems.

\---

## TC-14 Usability: first-time users (NFR-04, target ≤ 5 minutes each)

**Setup:** the app running (`py manage.py runserver` or Docker), `sample\_data/iris.csv` available on the participant's machine, a stopwatch.

**Participants:** 3 people who have **not** used the app before (friends or classmates outside the team). Tell them only:

> "This is a tool for testing machine-learning models on a CSV file. Please create an account, upload the file
> iris.csv, set it up to predict the species column, train any one model, and show me its accuracy.
> Think aloud. I can't help you while you do it."

Start the stopwatch when they open the home page; stop it when they point at the accuracy on the results page.

|#|Participant (first name or P1-P3)|Basic ML knowledge? (Y/N)|Time (mm:ss)|Finished without help? (Y/N)|Where they hesitated / comments|
|-|-|-|-|-|-|
|1|Johan |N|03:55|Y|-|
|2|Praneetha|Y|2:47|Y|-|
|3|Anusha|Y|2:32|Y|-|

**Result:** Pass 

## **Improvements suggested by participants** (add them as issues or to Sprint 2 notes):

\---

## TC-15 Cross-browser compatibility (NFR-05)

Run these three test cases in each browser (latest version). Mark ✅ if every step works and the layout looks right, ❌ otherwise and describe the problem.

|Test case|What to do|Chrome|Brave|Edge|
|-|-|-|-|-|
|TC-03 Login/logout|Register → log in → log out → press Back (should not show your data)|✅|✅|✅|
|TC-04 Upload + preview|Upload `sample\_data/iris.csv` → preview shows 20 rows and column types|✅|✅|✅|
|TC-07 Train + metrics|Configure (target `species`, 4 features) → train Logistic Regression and Random Forest → metrics and confusion matrix shown|✅|✅|✅|
|Compare (FR-14)|History → tick both → Compare selected → table and bar chart shown|✅|✅|✅|
|Export (FR-15)|Results → Download PDF and CSV → both files open|✅|✅|✅|

**Browser versions used:** Chrome Version 157.0.8103.40 (Official Build) (64-bit) · Firefox 160.0 (64-bit)  · Edge Version 157.0.4341.42 (Official build) (64-bit) (Menu → Help → About)

**Result:** Pass 

## **Problems found:**

\---



