import csv
import pylev
import string
import pandas
import argparse
import fuzzywuzzy
from time import sleep
from fuzzywuzzy import fuzz

exclude = set(string.punctuation)
second_look_words = set(['university','health','corporation','group','the','bank','energy','technologies','medical',
                         'systems','healthcare','solutions','school','marketing','global','entertainment','credit',
                         'city','union','media', 'financial','district','construction','of','worldwide','technology',
                         'system','services','pharmaceuticals','national','international','insurance','education',
                         'company','capital'])

second_look_words_cap = [w.capitalize() for w in second_look_words]

def write_to_files(file, vars):
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(vars)
    f.close

def levenshtein(a, b):
    len_a = len(a)
    len_b = len(b)
    distance = pylev.levenshtein(a, b)
    try:
        maxLength = max(len_a, len_b)
        result = maxLength - distance
        percentage = (result / maxLength) * 100
        return percentage
    except:
        return 0

def testFuncNew(text):
    return ' '.join([word for word in text.split() if word not in second_look_words and word not in second_look_words_cap])

def is_equal(a,b):
    if a == b:
        return 0
    else:
        return 1

def first_word(a,b):
    if (len(a) > 0) and (len(b) > 0):
        ratio = fuzz.ratio(a[0], b[0])
        if (ratio == 100) and (a[0] in second_look_words):
            return 0
        else:
            return ratio
    else:
        return 0

def camel_case_contains(a,b):
    if str(a).lower() in b:
        return 1
    else:
        return 0

def containment(a,b):
    if (len(a) == 1):
        if len(str(a[0])) > 2:
            if str(a[0]).lower() in b:
                return 1
            else:
                return 0
        return 0
    else:
        return 0

def first_word_rule_check(a):
    result = []
    if a > 88:
        result.append(a)
        result.append(1)
        return result
    else:
        result.append(a)
        result.append(0)
        return result

def camel_case_rule_check(a,b):
    if (a > 94) or (b > 94):
        return 1
    else:
        return 0

def camel_case_contained_rule_check(a,b):
    if (a == 1) or (b == 1):
        return 1
    else:
        return 0

def full_containment_rule_check(a,b):
    if (a == 1) or (b == 1):
        return 1
    else:
        return 0

def set_union_rule_check(a,t):
    results = []
    if a > t:
        results.append(a)
        results.append(1)
        return results
    else:
        results.append(a)
        results.append(0)
        return results

def are_companies_the_same(a):
    if a > 0:
        return 'YES'
    else:
        return 'NO'

def is_first_word_anywhere(a, b):
    ratios = []
    results = []
    if (len(a) > 0) and (len(b) > 0):
        for i in b:
            ratios.append(int(fuzz.ratio(str(i).lower(), str(a[0]).lower())))
        confidence = max(ratios)
        if confidence > 74:
            results.append(confidence)
            results.append(1)
            return results
        # elif any(a[0] in i for i in b):
        #     results.append('100')
        #     results.append(1)
        #     return results
        else:
            results.append(confidence)
            results.append(0)
            return results
    else:
        results.append(0)
        results.append(0)
        return results

def equate(a,b):
    if a != '-':
        if str(a) == str(b):
            return 'YES'
        else:
            return  'NO'
    else:
        return 'NO'

def count_them(i):
    n = names.count(i)
    return n

def lionel_enrichie(id, name_a, name_b):
    # format compared objects
    d = ''.join(ch for ch in str(name_a).replace("/",' ').replace("-",' ').lower() if ch not in exclude)
    dU = ''.join(ch for ch in str(name_a) if ch not in exclude)
    o = ''.join(ch for ch in str(name_b).replace("/",' ').replace("-",' ').lower() if ch not in exclude)
    oU = ''.join(ch for ch in str(name_b) if ch not in exclude)
    d_name = ''.join(ch for ch in str(d).lower() if ch not in exclude)
    o_name = ''.join(ch for ch in str(o).lower() if ch not in exclude)
    # length of both objects
    ld = len(d_name)
    lo = len(o_name)
    # check for presence of stopwords
    d_stopwords_out = testFuncNew(d_name)
    d_has_stopwords = is_equal(d_name, d_stopwords_out)
    o_stopwords_out = testFuncNew(o_name)
    o_has_stopwords = is_equal(o_name, o_stopwords_out)
    # create list objects
    d_name_list = str(d_name).split()
    d_name_stopword_out_list = str(d_stopwords_out).split()
    o_name_list = str(o_name).split()
    o_name_stopword_out_list = str(o_stopwords_out).split()
    lists = [d_name_list, d_name_stopword_out_list, o_name_list, o_name_stopword_out_list]
    # FIRST WORD RULE CRITERIA
        # first word match with stopwords
    first_word_all_words = first_word(d_name_list, o_name_list)
        # first word match with no stopwords
    first_word_stops_removed = first_word(d_name_stopword_out_list, o_name_stopword_out_list)
        # overall first word confidence
    first_word_confidence = max(first_word_all_words, first_word_stops_removed)
        # is first word anywhere in list
    fw_d_in_o = is_first_word_anywhere(d_name_stopword_out_list, o_name_list)
    fw_o_in_d = is_first_word_anywhere(o_name_stopword_out_list, d_name_list)
    # detect camel casing
        # with stopwords
    d_camel = ''.join([c for c in str(name_a) if c.isupper()])
    o_camel = ''.join([c for c in str(name_b) if c.isupper()])
        # with no stopwords
    d_camel_no_stopwords = ''.join([c for c in str(testFuncNew(dU)) if c.isupper()])
    o_camel_no_stopwords = ''.join([c for c in str(testFuncNew(oU)) if c.isupper()])
    # CAMEL CASE RULES CRITERIA
        #condition A
    camel_case_confidence_has_stopwords = fuzz.ratio(d_camel_no_stopwords, o_camel_no_stopwords)
    camel_case_confidence_no_stopwords = fuzz.ratio(d_camel_no_stopwords, o_camel_no_stopwords)
        #condition B
    d_camel_in_oxy = camel_case_contains(d_camel, o_name_list)
    o_camel_in_dorg = camel_case_contains(o_camel, d_name_list)
    # CONTAINMENT RULE CHECK
    d_contained_in_oxy = containment(d_name_list, o_name_list)
    o_contained_in_d = containment(o_name_list, d_name_list)
    # SET UNIONS
        # stopwords remain
    d_set_union_o_stopwords_remain = fuzz.token_set_ratio(d_name, o_name)
    o_set_union_d_stopwords_remain = fuzz.token_set_ratio(o_name, d_name)
    stopwords_remain_average = int((d_set_union_o_stopwords_remain + o_set_union_d_stopwords_remain) / 2)
        # stopwords removed from both sides
    d_set_union_o_no_stopwords = fuzz.token_set_ratio(d_stopwords_out, o_stopwords_out)
    o_set_union_d_no_stopwords = fuzz.token_set_ratio(o_stopwords_out, d_stopwords_out)
    no_stopwords_average = int((d_set_union_o_no_stopwords + o_set_union_d_no_stopwords) / 2)
    # RULE VALIDATION
    rule_one_check = first_word_rule_check(first_word_confidence)
    first_word_rule_status = rule_one_check[1]
    first_word_rule_strength = rule_one_check[0]
    d_first_word_contained_status = fw_d_in_o[1]
    d_first_word_contained_strength = fw_d_in_o[0]
    o_first_word_contained_status = fw_o_in_d[1]
    o_first_word_contained_strength = fw_o_in_d[0]
    camel_case_status = camel_case_rule_check(camel_case_confidence_has_stopwords, camel_case_confidence_no_stopwords)
    camel_contained_status = camel_case_contained_rule_check(d_camel_in_oxy, o_camel_in_dorg)
    full_containment_status = full_containment_rule_check(d_contained_in_oxy, o_contained_in_d)
    set_union_rule_status_with_stopwords = set_union_rule_check(stopwords_remain_average, 86)
    set_union_rule_status_with_stopwords_status = set_union_rule_status_with_stopwords[1]
    set_union_rule_status_with_stopwords_strength = set_union_rule_status_with_stopwords[0]
    set_union_rule_status_no_stopwords = set_union_rule_check(no_stopwords_average, 70)
    set_union_rule_status_no_stopwords_status = set_union_rule_status_no_stopwords[1]
    set_union_rule_status_no_stopwords_strength = set_union_rule_status_no_stopwords[0]
    companies_match = are_companies_the_same(set_union_rule_status_no_stopwords_status +
                                             set_union_rule_status_with_stopwords_status +
                                             first_word_rule_status +
                                             camel_case_status +
                                             camel_contained_status +
                                             full_containment_status +
                                             o_first_word_contained_status +
                                             d_first_word_contained_status)
    match_total = max([first_word_rule_status, first_word_rule_strength,
            d_first_word_contained_status, d_first_word_contained_strength,
            o_first_word_contained_status, o_first_word_contained_strength,
            camel_case_status, camel_contained_status,
            full_containment_status,
            set_union_rule_status_with_stopwords_status, set_union_rule_status_with_stopwords_strength,
            set_union_rule_status_no_stopwords_status, set_union_rule_status_no_stopwords_strength])
    vars = [id,
            # dorg variables
            str(name_a), ld, d_stopwords_out, d_has_stopwords, d_camel, d_camel_no_stopwords,
            # oxy variables
            str(name_b), lo, o_stopwords_out,o_has_stopwords, o_camel, o_camel_no_stopwords,
            # rules variables
                #FIRST WORD RULE
            first_word_all_words, first_word_stops_removed, first_word_confidence,
                #CAMEL CASE RULE
            camel_case_confidence_has_stopwords, camel_case_confidence_no_stopwords, d_camel_in_oxy, o_camel_in_dorg,
                #CONTAINMENT RULE
            d_contained_in_oxy, o_contained_in_d,
                #SET UNION CONFIDENCES
            stopwords_remain_average, no_stopwords_average,
                # RULES RESULTS
            first_word_rule_status, first_word_rule_strength,
            d_first_word_contained_status, d_first_word_contained_strength,
            o_first_word_contained_status, o_first_word_contained_strength,
            camel_case_status, camel_contained_status,
            full_containment_status,
            set_union_rule_status_with_stopwords_status, set_union_rule_status_with_stopwords_strength,
            set_union_rule_status_no_stopwords_status, set_union_rule_status_no_stopwords_strength,
            # result
            match_total, companies_match]
    return vars


def main(input_file, id, first_object, second_object, outfile):
    data = pandas.read_csv(input_file)
    for index, row in data.iterrows():
        result = lionel_enrichie(id, row[first_object], row[second_object])
        write_to_files(outfile, result)



if __name__ == '__main__':
    # Command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input_file', help='The path to the file you want to run', required=True)
    parser.add_argument('-id', '--id', help='Column containing a Unique Row ID', required=True)
    parser.add_argument('-first_object', '--first_object', help='Column containing the first string object '
                                                                           'you want to compare', required=True)
    parser.add_argument('-second_object', '--second_object', help='Column containing the second string '
                                                                             'object you want to compare', required=True)
    parser.add_argument('-o', '--outfile', help='The path to the file you ', required=True)

    args = parser.parse_args()

    main(args.input_file, args.id, args.first_object, args.second_object, args.outfile)
