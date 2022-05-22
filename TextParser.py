#version 0.4
from R_O import verb0dict
from R_O import verb1dict
from R_O import verb2dict
from R_O import verblitdict
from R_O import verblit2dict
from R_O import verb2litdict
from R_O import noundict
from R_O import multinoundict
import R_O
import textwrap
import random
class History():

    pr_verb = '' #previous verb
    pr_d_o = '' #previous direct object
    pr_i_o = '' #previous indirect object
    pr_command = ''
    needs_specification = False #True if the previous command was a specification error
    d_o_needs_disambiguation = False #True if the previous command had a disambiguation error for the direct object
    i_o_needs_disambiguation = False #True if the previous command had a disambiguation error for the indirect object

def pront(text): #printing, but with wrapped text (will not work for blank lines, use print() instead)
    print(textwrap.fill(text, width = 80))

def prompt_for_command(): #prompts input from the player, also converts to lowercase
    raw_command = input('> ')
    return raw_command.lower()

def purge_articles(target): #removes all articles ("the," "a," "an") from a string
    new_command = target
    new_command = ' ' + new_command + ' '
    while ((((' the ' in new_command) or ' a ' in new_command) or ' an ' in new_command) or '  ' in new_command):
        new_command = new_command.replace(' the ', ' ')
        new_command = new_command.replace(' a ', ' ')
        new_command = new_command.replace(' an ', ' ')
        new_command = new_command.replace('  ', ' ')
    return new_command.strip()

def interpret_command(target):
    verb = '' #local verb
    d_o = '' #local direct object
    i_o = '' #local indirect object

    def report_history():
        History.pr_verb = verb; History.pr_d_o = d_o; History.pr_i_o = i_o; History.pr_command = verbatim_command

    def verb_lits_purge_article(new_command):
        while (((new_command.startswith('the ') or new_command.startswith('a ')) or new_command.startswith('an ')) or new_command.startswith(' ')):
            if new_command.startswith('the '):
                new_command = new_command[4:]
            elif new_command.startswith('a '):
                new_command = new_command[2:]
            elif new_command.startswith('an '):
                new_command = new_command[3:]
            elif new_command.startswith(' '):
                new_command = new_command[1:]
        return new_command

    verbatim_command = target #unchanged version of the command, complete with articles
    standard_command = purge_articles(target) #command without articles, used for nonliteral verbs
    loop_dict = noundict.copy(); loop_dict.update(multinoundict) #dictionary for looping over both nouns and multinouns
    if History.d_o_needs_disambiguation and standard_command in loop_dict:
        if standard_command in noundict: #update the direct object if there is a matching noun
            d_o = noundict[standard_command]
        else:                            #or a matching multinoun
            d_o = stringify_tuple(multinoundict[standard_command])
        History.pr_d_o = d_o
        History.d_o_needs_disambiguation = False
        return ((History.pr_verb + ' ' + History.pr_d_o + ' ' + History.pr_i_o).strip())
    if History.i_o_needs_disambiguation and standard_command in loop_dict:
        if standard_command in noundict: #update the indirect object if there is a matching noun
            i_o = noundict[standard_command]
        else:                            #or a matching multinoun
            i_o = stringify_tuple(multinoundict[standard_command])
        History.pr_i_o = i_o
        History.i_o_needs_disambiguation = False
        return ((History.pr_verb + ' ' + History.pr_d_o + ' ' + History.pr_i_o).strip())
    History.d_o_needs_disambiguation = False
    History.i_o_needs_disambiguation = False
    if standard_command in verb0dict: #if the command is a zero valent verb
        if verb0dict[standard_command] == 'again':
            return interpret_command(History.pr_command)
        verb = verb0dict[standard_command]; d_o = ''; i_o = '' #set the verb to the id from the dictionary, clear objects
        History.needs_specification = False #successful command, so no more specification needed
        report_history() #update the history
        return verb
    for x in verb1dict:
        if standard_command.startswith(x + ' '): #if the command is a monovalent verb
            predicate = standard_command[len(x) + 1:] #predicate is the rest of the input after the verb
            verb = verb1dict[x] #update the current verb if there is a match
            if (predicate in noundict) or (predicate in multinoundict):
                if predicate in noundict: #update the direct object if there is a matching noun
                    d_o = noundict[predicate]
                else:                     #or a matching multinoun
                    d_o = stringify_tuple(multinoundict[predicate])
                i_o = '' #clear indirect object, verb and direct object already set
                History.needs_specification = False #successful command, so no more specification needed
                report_history() #update the history
                return(verb + ' ' + d_o)
    for x in verb2dict:
        if standard_command.startswith(x + ' '): #if the command is a divalent verb
            predicate = standard_command[len(x) + 1:] #predicate is the rest of the input after the verb
            verb = verb2dict[x][0] #update the current verb if there is a match
            for y in loop_dict:
                if predicate.startswith(y + ' '): #if the predicate starts with a noun
                    predicate = predicate[len(y) + 1:] #predicate is updated, noun is removed
                    if y in noundict: #update the direct object if there is a matching noun
                        d_o = noundict[y]
                    else:                     #or a matching multinoun
                        d_o = stringify_tuple(multinoundict[y])
                    for z in verb2dict[x][1]: #check prepositions for the verb
                        if predicate.startswith(z):
                            predicate = predicate[len(z) + 1:]  #if the preposition is found, cut it off the predicate and proceed
                            if (predicate in noundict) or (predicate in multinoundict):
                                if predicate in noundict: #update the indirect object if there is a matching noun
                                    i_o = noundict[predicate]
                                else:                     #or a matching multinoun
                                    i_o = stringify_tuple(multinoundict[predicate])
                                History.needs_specification = False #successful command, so no more specification needed
                                report_history() #update the history
                                return(verb + ' ' + d_o + ' ' + i_o)
    mod_verbatim_command = verb_lits_purge_article(verbatim_command) #modify the verbatim command to work with literal verbs, only remove articles from the front
    for x in verblitdict:
        if mod_verbatim_command.startswith(x + ' '): #if the command is a literal verb
            verb = verblitdict[x] #update current verb if there is a match
            d_o = mod_verbatim_command[len(x) + 1 :] #the rest of the command is the direct object
            i_o = '' #clear indirect object, verb and direct object are set
            History.needs_specification = False #successful command, so no more specification needed
            report_history() #update the history
            return (verb + ' ' + d_o.replace(' ','_')) #underscore is necessary for some messy coding in executer.py
    for x in verblit2dict:
        if mod_verbatim_command.startswith(x + ' '): #if the command is a verb with a literal and then a noun
            verb = verblit2dict[x][0] #update current verb if there is a match
            predicate = standard_command[len(x) + 1 :]
            for y in loop_dict:
                if predicate.endswith(' ' + y):
                    if y in noundict: #update the direct object if there is a matching noun
                        i_o = noundict[y]
                    else:             #or a matching multinoun
                        i_o = stringify_tuple(multinoundict[y])
                    predicate = predicate[:-len(y) - 1]
                    for z in verblit2dict[x][1]:
                        if predicate.endswith(' ' + z):
                            d_o = predicate[:-len(z) - 1].replace(' ', '_') #underscore is necessary for some messy coding in executer.py
                            History.needs_specification = False #successful command, so no more specification needed
                            report_history() #update the history
                            return (verb + ' ' + d_o + ' ' + i_o)
    for x in verb2litdict:
        if mod_verbatim_command.startswith(x + ' '): #if the command is a verb with a noun and then a literal
            verb = verb2litdict[x][0] #update current verb if there is a match
            predicate = standard_command[len(x) + 1 :]
            for y in loop_dict:
                if predicate.startswith(y + ' '):
                    if y in noundict: #update the direct object if there is a matching noun
                        d_o = noundict[y]
                    else:             #or a matching multinoun
                        d_o = stringify_tuple(multinoundict[y])
                    predicate = predicate[len(y) + 1 :]
                    for z in verb2litdict[x][1]:
                        if predicate.startswith(z + ' '):
                            i_o = predicate[len(z) + 1 :].replace(' ', '_') #underscore is necessary for some messy coding in executer.py
                            History.needs_specification = False #successful command, so no more specification needed
                            report_history() #update the history
                            return (verb + ' ' + d_o + ' ' + i_o)
    for x in verblit2dict:
        if mod_verbatim_command.startswith(x + ' '):
            verb = verblit2dict[x][0] #update the verb
            d_o = mod_verbatim_command[len(x) + 1:]
            print(d_o)
            temp_error = History.pr_d_o #store the value of the previous direct object in case an error message needs to be generated
            History.needs_specification = True #failed command, so more specification needed
            report_history() #update the history
            return ('#You should specify ' + after_(verb) + ' what you wish to ' + before_(verb) + ' "' + d_o + '."').replace('|', ' ')
    for x in verb2litdict:
        if mod_verbatim_command.startswith(x + ' '):
            verb = verb2litdict[x][0] #update the verb
            predicate = mod_verbatim_command[len(x) + 1:]
            if predicate in loop_dict:
                if predicate in noundict: #update the indirect object if there is a matching noun
                    d_o = noundict[predicate]
                else:                     #or a matching multinoun
                    d_o = stringify_tuple(multinoundict[predicate])
                History.needs_specification = True #failed command, so more specification needed
                report_history() #update the history
                return ('#You should specify ' + after_(verb) + ' what you wish to ' + before_(verb) + ' the ' + predicate + '.').replace('|', ' ')
            History.needs_specification = False #nonsense command, so more specification impossible
            report_history() #update the history
            return ('#You cannot ' + before_(verb) + ' the ' + predicate + ' because there is no ' + predicate + ' here.').replace('|', ' ')
    if standard_command in verblitdict: #if the command is a bare literal verb
        verb = verblitdict[standard_command] #update the verb
        History.needs_specification = True #failed command, so more specification needed
        report_history() #update the history
        return ('#You should specify what you want to ' + verblitdict.get(standard_command) + '.').replace('|', ' ') #return an error message
    elif standard_command in verblit2dict:
        verb = verblit2dict[standard_command] #update the verb
        History.needs_specification = True #failed command, so more specification needed
        report_history() #update the history
        return ('#You should specify what you want to ' + before_(verblit2dict.get(standard_command)[0]) + '.').replace('|', ' ')
    elif standard_command in verb2litdict:
        verb = verb2litdict[standard_command] #update the verb
        History.needs_specification = True #failed command, so more specification needed
        report_history() #update the history
        return ('#You should specify what you want to ' + before_(verb2litdict.get(standard_command)[0]) + '.').replace('|', ' ')
    elif standard_command in verb1dict:
        verb = verb1dict[standard_command] #update the verb
        History.needs_specification = True #failed command, so more specification needed
        report_history() #update the history
        return ('#You should specify what you wish to ' + verb1dict[standard_command] + '.').replace('|', ' ')
    elif standard_command in verb2dict:
        verb = verb2dict[standard_command] #update the verb
        History.needs_specification = True #failed command, so more specification needed
        report_history() #update the history
        return ('#You should specify what you wish to ' + before_(verb2dict[standard_command][0]) + '.').replace('|', ' ')
    for x in verb2dict:
        if standard_command.startswith(x + ' '):
            predicate = standard_command[len(x) + 1:] #predicate is the rest of the input after the verb
            verb = verb2dict[x][0] #update the current verb if there is a match
            if predicate in loop_dict:
                if predicate in noundict: #update the direct object if there is a matching noun
                    d_o = noundict[predicate]
                else:                     #or a matching multinoun
                    d_o = stringify_tuple(multinoundict[predicate])
                History.needs_specification = True #failed command, so more specification needed
                report_history() #update the history
                return ('#You should specify ' + after_(verb) + ' what you wish to ' + before_(verb) + ' the ' + predicate + '.').replace('|', ' ')
            for y in loop_dict:
                if predicate.startswith(y + ' '): #if the predicate starts with a noun
                    predicate = predicate[len(y) + 1:] #predicate is updated, noun is removed
                    if y in noundict: #update the direct object if there is a matching noun
                        d_o = noundict[y]
                    else:                     #or a matching multinoun
                        d_o = stringify_tuple(multinoundict[y])
                    if predicate in verb2dict[x][1]:
                        History.needs_specification = True #failed command, so more specification needed
                        verbatim_command = verbatim_command [: - (len(predicate) + 1)]
                        report_history() #update the history
                        return ('#You should specify ' + after_(verb) + ' what you wish to ' + before_(verb) + ' the ' + y + '.').replace('|', ' ')
                    for z in verb2dict[x][1]:
                        if predicate.startswith(z + ' '):
                            i_o = predicate[len(z) + 1 :]
                            History.needs_specification = False #nonsense command, so more specification impossible
                            report_history() #update the history
                            if R_O.verb_id_dict[verb].get_i_o_requires_sight():
                                return ('#You cannot ' + before_(verb) + ' the ' + y + ' ' + after_(verb) + ' the ' + i_o + ' because there is no ' + i_o + ' here.').replace('|', ' ')
                            else:
                                return ('#You have not seen any ' + i_o + '.')
                    History.needs_specification = False #nonsense command, so more specification impossible
                    report_history() #update the history
                    return ('#Nothing after wanting to ' + before_(verb) + ' the ' + y + ' makes sense.')
            return('#You cannot ' + before_(verb) + ' the ' + predicate + ' because there is no ' + predicate + ' here.').replace('|', ' ')
    for x in verb1dict:
        if standard_command.startswith(x + ' '):
            d_o = standard_command[len(x) + 1:]
            i_o = ''
            History.needs_specification = False #nonsense command, so more specification impossible
            report_history() #update the history
            return ('#You cannot ' + verb1dict[x] + ' the ' + d_o + ' because there is no ' + d_o + ' here.').replace('|', ' ')
    if History.needs_specification: #check to see if the player is correcting a specification error
        prep = ''
        if History.pr_d_o != '':
            prep = after_(History.pr_verb)
        if purge_articles(verbatim_command).strip() in loop_dict:
            verbatim_command = purge_articles(verbatim_command) #redo interpretation with no articles if it's a noun
        verbatim_command = (History.pr_command + ' ' + prep).strip() + ' ' + verbatim_command
        return interpret_command(verbatim_command) #redo the interpretation
    return '#Your command does not contain a valid verb.'

def disambiguate_command(target): #deals with ambiguous commands, like "get ball" if there are two balls present
    if target[0] == '#': #do not disambiguate error messages
        return target
    alist = target.split(' ')
    blist = []
    if len(alist) == 1: #if the list has a single verb, do not disambiguate (only nouns)
        return [target]
    elif len(alist) == 2:
        blist.append(alist[0])
        q = R_O.verb_id_dict[alist[0]].disambiguate(alist[1])
        if q[0] == '#':
            return q
        elif type(q) == str:
            blist.append(q)
            return blist
        if len(q) == 1:
            blist.append(q[0])
        else:
            y = []
            for x in q:
                y.append(x.get_name())
            n = R_O.beautify_sequence(y, 'or')
            History.d_o_needs_disambiguation = True
            return('#You should specify whether you mean ' + beautify_noun(n) + '.')
        return blist
    else:
        blist.append(alist[0])
        q = R_O.verb_id_dict[alist[0]].disambiguate_d_o(alist[1])
        if q[0] == '#':
            return q
        elif type(q) == str:
            blist.append(q)
        if len(q) == 1 or type(q) == str:
            if type(q) != str:
                blist.append(q[0])
            r = R_O.verb_id_dict[alist[0]].disambiguate_i_o(q[0], alist[2])
            if r[0] == '#':
                return r
            elif type(r) == str:
                blist.append(r)
                return blist
            if len(r) == 1:
                blist.append(r[0])
            else:
                y = []
                for x in r:
                    y.append(x.get_name())
                n = R_O.beautify_sequence(y, 'or')
                History.i_o_needs_disambiguation = True
                return('#You should specify whether you mean ' + beautify_noun(n) + '.')
            return blist
        else:
            y = []
            for x in q:
                y.append(x.get_name())
            n = R_O.beautify_sequence(y, 'or')
            History.d_o_needs_disambiguation = True
            return('#You should specify whether you mean ' + beautify_noun(n) + '.')
        return blist

def before_(text):
    return (text[:text.index('_')])

def after_(text):
    return (text[text.index('_') + 1:])

def beautify_noun(text):
    text = text.replace('_', ' ')
    if '#' in text:
        return (text[:text.index('#')])
    return text

def stringify_tuple(input):
    output = ''
    for x in input:
        output += '~'; output += x
    return output[1:]

def parse():
        q = interpret_command(prompt_for_command())
        q = disambiguate_command(q)
        return q
