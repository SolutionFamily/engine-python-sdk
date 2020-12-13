# Release Process for SDK

If you're a Python dev, you might wonder why this file is here. Since Python is not our day-to-day tool chain, these are notes to remind us on how to do a release without having to use a search engine every time.

0. Delete all files in the `dist` and `build` folders
1. Update the `version` in `setup.py`
2. Build the distribution package
    ```
    $ python setup.py sdist bdist_wheel
    ```
3. Sanity-check the package
   ```
   $ twine check dist/*
   ```
4. Test publish
   ```
   $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```
5. Check the publish result at  https://test.pypi.org/project/solutionfamily/
6. If all is goo, publish publicly
   ```
   $ twine upload dist/*
   ```