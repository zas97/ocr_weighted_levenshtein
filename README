# Ocr weighted Levenshtein distance

## Getting started

To install the library :

    pip install ocr-weighted-levenshtein weighted-levenshtein

### Usage

```python
    import ocr_weighted_levenhstein
    from weighted_levenshtein import lev

    leven_params = ocr_weighted_levenhstein.get_distances_params()

    ## The order of parameters matter
    # lev("word_in_ocr", "word_to_match", **leven_params)

    print(lev("rat", "cat", **leven_params)) ## prints 1.16
    print(lev("eat", "cat", **leven_params)) ## prints 0.57
    print(lev("Bat", "8at", **leven_params)) ## prints 0.46
    print(lev("hello", "hell0", **leven_params)) ## prints 0.13
    print(lev("What", "what", **leven_params)) ## prints 0.26
    print(lev("hello", "helloi", **leven_params)) ## prints 0.24
    print(lev("hello", "helloH", **leven_params)) ## prints 0.83
``` 

## Use Cases

The Levenshtein distance is often used to search words in ocrised texts in fault tolerant manner. For example if we are searching for the word THEATRE in an image with text the ocr will sometimes recognize words like THEATRF or T4EATRE. To match also this words a common tactic is to search any word that is at a Levenshtein distance 1 from THEATRE. However, in this use case not all edit operation should have the same cost, the word THEATRF should be closer to the word THEATRW since the ocr is more likely to confuse an F from E than a W from an E.



