#version 0.4
import textwrap
import random

verb0dict = {}
verb1dict = {}
verb2dict = {}
verblitdict = {}
verblit2dict = {}
verb2litdict = {}
noundict = {}
multinoundict = {}

noun_id_dict = {}
verb_id_dict = {}

directions = ['n','s','w','e','nw','ne','sw','se','u','d']

pronouns = ['they', 'he', 'she', 'it', 'you']

directionsdict = {
    'n' : 'north',
    's' : 'south',
    'w' : 'west',
    'e' : 'east',
    'nw' : 'northwest',
    'ne' : 'northeast',
    'sw' : 'southwest',
    'se' : 'southeast',
    'u' : 'up',
    'd' : 'down'
}

pluralsdict = {
    'is' : 'are',
    'Is' : 'Are',
    'it' : 'they',
    'It' : 'They',
    'he' : 'they',
    'He' : 'They',
    'she' : 'they',
    'She' : 'They',
    'this' : 'these',
    'This' : 'These',
    'that' : 'those',
    'That' : 'Those'

}

obliquesdict = {
    'they' : 'them',
    'he' : 'him',
    'she' : 'her',
    'who' : 'whom',
    'I' : 'me',
    'we' : 'us',
    'They' : 'Them',
    'He' : 'Him',
    'She' : 'Her',
    'Who' : 'Whom',
    'We' : 'Us'
}

reflexivesdict = {
    'they' : 'themself',
    'he' : 'himself',
    'she' : 'herself',
    'it' : 'itself',
    'we' : 'ourself',
    'you' : 'yourself',
    'I' : 'myself',
    'They' : 'Themself',
    'He' : 'Himself',
    'She' : 'Herself',
    'It' : 'Itself',
    'We' : 'Ourself',
    'You' : 'Yourself',
}

posessivesdict = {
    'they' : 'theirs',
    'he' : 'his',
    'she' : 'hers',
    'it' : 'its',
    'we' : 'our',
    'you' : 'your',
    'who' : 'whose',
    'I' : 'my',
    'They' : 'Theirs',
    'He' : 'His',
    'She' : 'Hers',
    'It' : 'Its',
    'We' : 'Our',
    'You' : 'Your',
    'Who' : 'Whose',
}

def define_pronoun(nom, obl, ref, pos): #create and add more pronouns if you so wish, or redefine and modify existing pronouns
    if nom not in pronouns: #unfortunately no duplicates allowed (wouldn't work with dictionary structures)
        pronouns.append(nom)
    obliquesdict[nom] = obl
    reflexivesdict[nom] = ref
    posessivesdict[nom] = pos

def a_an(word):
    assert type(word) == str, 'The word must be a string.'
    vowels = ['a','e','i','o','u']
    if word[0].lower() in vowels:
        return 'an ' + word
    return 'a ' + word

def test_a_an(word):
    assert type(word) == str, 'The word must be a string.'
    vowels = ['a','e','i','o','u']
    if word[0].lower() in vowels:
        return 'an'
    return 'a'

def obliquefy(phrase):
    l = phrase.split(' ')
    b = ''
    for word in l:
        if word in obliquesdict:
            b += obliquesdict[word]; b += ' '
        else:
            b += word; b += ' '
    return b[:-1]

def reflexify(phrase):
    l = phrase.split(' ')
    b = ''
    for word in l:
        if word in reflexivesdict:
            b += reflexivesdict[word]; b += ' '
        else:
            b += word; b += ' '
    return b[:-1]

def posessify(phrase):
    l = phrase.split(' ')
    b = ''
    for word in l:
        if word in posessivesdict:
            b += posessivesdict[word]; b += ' '
        else:
            b += word; b += ' '
    return b[:-1]

class Room:
    def __init__(self):
        self.desc = 'This is a nondescript room.'
        self.dark = False
        self.dark_desc = 'This is a dark place.'
        self.sound_desc = 'You hear nothing.'
        self.smell_desc = 'You smell nothing.'
        self.contents = []
        self.exits = {}
        self.nexits = {}
        for x in directions:
            if (x not in self.exits) and (x not in self.nexits):
                self.nexits[x] = 'You cannot go in that direction.'

    def add_exit(self, dir, dest, msg):
        assert dir in directions, 'The supplied direction is invalid.'
        assert isinstance(dest, Room), 'The supplied destination is not a room.'
        assert type(msg) == str, 'The travel message must be a string.'
        self.exits[dir] = (dest, msg)
        if dir in self.nexits:
            self.nexits.pop(dir)

    def add_nexit(self, dir, msg):
        assert dir in directions, 'The supplied direction is invalid.'
        assert type(msg) == str, 'The obstruction message must be a string.'
        self.nexits[dir] = msg
        if dir in self.exits:
            self.exits.pop(dir)

    def make_all_nexit_defaults(self, msg):
        assert type(msg) == str, 'The obstruction message must be a string.'
        for x in directions:
            if (x not in self.exits):
                self.nexits[x] = msg

    def add_door(self, dir, door):
        assert dir in directions, 'The supplied direction is invalid.'
        assert isinstance(door, Door), 'The supplied door is not actually a door.'
        self.exits[dir] = (door, door.get_move_message())
        if dir in self.nexits:
            self.nexits.pop(dir)

    def travelcheck(self, dir):
        assert dir in directions, 'The supplied direction is invalid.'
        return True

    def set_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.desc = desc

    def set_dark_desc(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.dark_desc = desc

    def set_sound_description(self, desc):
        assert type(desc) == str or isinstance(desc, Perception), 'The description must be a string or a perception.'
        self.sound_desc = desc

    def set_smell_description(self, desc):
        assert type(desc) == str or isinstance(desc, Perception), 'The description must be a string or a perception.'
        self.smell_desc = desc

    def get_exits(self):
        return self.exits

    def get_nexits(self):
        return self.nexits

    def get_contents(self):
        return self.contents

    def is_noisy(self):
        if isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
            return True
        else:
            for x in self.get_contents():
                if x.is_noisy():
                    return True
        return False

    def is_smelly(self):
        if isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
            return True
        else:
            for x in self.get_contents():
                if x.is_smelly():
                    return True
        return False

    def describe_sound(self, implicit = False):

        def report_ambient_sounds(thing, implicit2 = False):
            if (isinstance(thing, Container) and (thing.is_transparent_sound() or thing.is_open())) or isinstance(thing, Room):
                for x in thing.get_contents():
                    if (not implicit2) or x != player:
                        report_ambient_sounds(x)
            if isinstance(thing.sound_desc, Perception) and thing.sound_desc.get_activity():
                if isinstance(thing, Room) or thing.is_visible():
                    pront(thing.sound_desc.get_description())
                else:
                    pront(thing.sound_desc.get_invisible_description())

        if self.is_noisy():
            report_ambient_sounds(self, implicit)
        else:
            if isinstance(self.sound_desc, str):
                pront(self.sound_desc)
            elif isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
                if self.is_visible():
                    pront(self.sound_desc.get_description())
                else:
                    pront(self.sound_desc.get_invisible_description())

    def describe_smell(self, implicit = False):

        def report_ambient_smells(thing, implicit2 = False):
            if (isinstance(thing, Container) and (thing.is_transparent_smell() or thing.is_open())) or isinstance(thing, Room):
                for x in thing.get_contents():
                    if (not implicit2) or x != player:
                        report_ambient_smells(x)
            if isinstance(thing.smell_desc, Perception) and thing.smell_desc.get_activity():
                if isinstance(thing, Room) or thing.is_visible():
                    pront(thing.smell_desc.get_description())
                else:
                    pront(thing.smell_desc.get_invisible_description())

        if self.is_smelly():
            report_ambient_smells(self, implicit)
        else:
            if isinstance(self.smell_desc, str):
                pront(self.smell_desc)
            elif isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
                pront(self.smell_desc.get_description())

    def make_dark(self):
        self.dark = True

    def make_lit(self):
        self.dark = False

    def is_dark(self):
        return self.dark

    def is_illuminated(self):
        if self.is_dark():
            for x in self.get_contents():
                if x.is_illuminated():
                    return True
        else:
            return True

    def describe(self):
        if self.is_illuminated():
            pront(self.desc)
            for x in self.get_contents():
                if x != player and not isinstance(x, NPC) and 'hidden' not in x.get_properties():
                    if 'initialize' in x.get_properties():
                        pront(x.init_desc)
                    elif ('unlisted' in x.get_properties()) and isinstance(x, Surface) and len(x.get_contents()) > 0:
                        pront(f'{x.art_d().capitalize()} {x.pluralize("bears")}:')
                        x.list_contents(1)
                    elif ('unlisted' in x.get_properties()) and isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()):
                        pront(f'{x.art_d().capitalize()} {x.pluralize("contains")}:')
                        x.list_contents(1)
            for y in self.get_contents():
                w = ''
                if isinstance(y, RopeTrail) and y.is_visible():
                    k = y.get_parent_rope()
                    if k.get_tied_objects()[0].is_visible():
                        if 'plug' in k.get_properties():
                            w += f' (plugged into '
                        else:
                            w += f' (tied to '
                        if len(k.get_tied_objects()) == 1:
                            w += f'{k.get_tied_objects()[0].art_d()})'
                        elif len(k.get_tied_objects()) == 2:
                            w += f'{k.get_tied_objects()[0].art_d()} and {k.get_tied_objects()[1].art_d()})'
                        pront(f'There {k.pluralize("is")} {k.art_i()}{w} here.')
                    elif len(k.get_tied_objects()) > 1 and k.get_tied_objects()[1].is_visible():
                        if 'plug' in k.get_properties():
                            w += f' (plugged into '
                        else:
                            w += f' (tied to '
                        w += f'{k.get_tied_objects()[1].art_d()})'
                        pront(f'There {k.pluralize("is")} {k.art_i()}{w} here.')
                    else:
                        pront(f'There {k.pluralize("is")} {k.art_i()} running across the ground here.')
                if ('unlisted' not in y.get_properties()) and ('initialize' not in y.get_properties() and 'hidden' not in y.get_properties()):
                    if 'plug' in y.get_properties() and isinstance(y, Rope) and len(y.get_tied_objects()) > 0:
                        w += f' (plugged into '
                    elif isinstance(y, Rope):
                        w += f' (tied to '
                    if isinstance(y, Rope) and len(y.get_tied_objects()) == 1:
                        w += f'{y.get_tied_objects()[0].art_d()})'
                    if isinstance(y, Rope) and len(y.get_tied_objects()) == 2:
                        w += f'{y.get_tied_objects()[0].art_d()} and {y.get_tied_objects()[1].art_d()})'
                    if hasattr(y, 'parent_attachment'):
                        if 'plug' in y.get_properties():
                            w += f' (plugged into {y.get_parent_attachment().art_d()})'
                        else:
                            w += f' (attached to {y.get_parent_attachment().art_d()})'
                    if 'lamp' in y.get_properties() and y.get_brightness() == 2:
                        w += ' (lit)'
                    pront(f'There {y.pluralize("is")} {y.art_i()}{w} here.')
                    if isinstance(y, Surface) and len(y.get_contents()) > 0:
                        pront(f'{y.art_d().capitalize()} {y.pluralize("bears")}:')
                        y.list_contents(1)
                    elif isinstance(y, Container) and len(y.get_contents()) > 0 and (y.is_open() or y.is_transparent()):
                        pront(f'{y.art_d().capitalize()} {y.pluralize("contains")}:')
                        y.list_contents(1)
            for z in self.get_contents():
                if isinstance(z, NPC) and 'hidden' not in z.get_properties():
                    pront(z.get_activity_desc())
        else:
            pront(self.dark_desc)
            for x in self.get_contents():
                if x.get_brightness() == 1:
                    if x != player and not isinstance(x, NPC) and 'hidden' not in x.get_properties():
                        if 'initialize' in x.get_properties():
                            pront(x.init_desc)
                        elif ('unlisted' in x.get_properties()) and isinstance(x, Surface) and len(x.get_contents()) > 0:
                            pront(f'{x.art_d().capitalize()} {x.pluralize("bears")}:')
                            x.list_contents(1)
                        elif ('unlisted' in x.get_properties()) and isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()):
                            pront(f'{x.art_d().capitalize()} {x.pluralize("contains")}:')
                            x.list_contents(1)
            for y in self.get_contents():
                if y.get_brightness() == 1:
                    if ('unlisted' not in y.get_properties()) and ('initialize' not in y.get_properties() and 'hidden' not in y.get_properties()):
                        pront(f'There {y.pluralize("is")} {y.art_i()} here.')
                        if isinstance(y, Surface) and len(y.get_contents()) > 0:
                            pront(f'{y.art_d().capitalize()} {y.pluralize("bears")}:')
                            y.list_contents(1)
                        elif isinstance(y, Container) and len(y.get_contents()) > 0 and (y.is_open() or y.is_transparent()):
                            pront(f'{y.art_d().capitalize()} {y.pluralize("contains")}:')
                            y.list_contents(1)
            for z in self.get_contents():
                if y.get_brightness() == 1:
                    if isinstance(z, NPC) and 'hidden' not in z.get_properties():
                        pront(z.get_activity_desc())
        if self.is_noisy():
            self.describe_sound(True)
        if self.is_smelly():
            self.describe_smell(True)

offstage = Room()

class Object:

    def __init__(self, name, id, synonyms):
        assert type(name) == str, 'The name of the object must be a string.'
        assert type(id) == str, 'The internal id of the object must be a string.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.name = name
        self.id = id
        self.synonyms = synonyms
        for x in self.synonyms:
            if x in noundict:
                multinoundict[x] = (noundict[x], self.id)
                noundict.pop(x)
            elif x in multinoundict:
                temp = multinoundict[x]
                new = temp + (self.id,)
                multinoundict[x] = new
            else:
                noundict[x] = self.id
        noun_id_dict[self.id] = self
        self.desc = 'It is an ordinary ' + self.name + '.'
        self.loc = offstage
        self.loc.contents.append(self)
        self.properties = []
        self.bulk = 10
        self.brightness = 0
        self.components = []
        self.allowed_parent_attachments = []
        self.allowed_child_attachments = []
        self.child_attachments = []
        self.known = False
        self.custom_immobile_message = 'It cannot be moved.'
        self.remaps_d = {}
        self.remaps_i = {}
        self.articles = ['the', test_a_an(self.name)]
        self.plural = False
        self.pronoun = 'it'
        self.sound_desc = 'You hear nothing.'
        self.smell_desc = 'You smell nothing.'
        self.touch_desc = 'You feel nothing unusual.'
        self.taste_desc = 'You taste no distinct flavor.'
        self.read_desc = 'Nothing is written there.'


    def set_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.desc = desc

    def set_initial_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.init_desc = desc

    def get_initial_description(self):
        return self.init_desc

    def swap_name(self, name):
        assert type(name) == str, 'The new name must be a string.'
        self.name = name

    def warp_to(self, loc):
        assert isinstance(loc, Room) or isinstance(loc, Container), 'The target location must be a room or container.'
        for x in self.get_child_attachments():
            if not(isinstance(x, Rope) and len(x.get_tied_objects()) > 1 and x.get_tied_objects()[0].is_within(player) and x.get_tied_objects()[1].is_within(player)):
                x.warp_to(loc)
        self.loc.contents.remove(self)
        self.loc = loc
        self.loc.contents.append(self)
        for x in self.get_components():
            x.warp_to(loc)
            if hasattr(x, 'parent_attachment'):
                x.detach()
        self.remove_property('worn')

    def drag_to(self, loc, r):
        assert isinstance(loc, Room) or isinstance(loc, Container), 'The target location must be a room or container.'
        assert isinstance(r, Rope), 'The dragging rope must be a rope.'
        self.loc.contents.remove(self)
        self.loc = loc
        self.loc.contents.append(self)
        for x in self.get_components():
            x.warp_to(loc)
            if hasattr(x, 'parent_attachment'):
                x.detach()
        for x in self.get_child_attachments():
            if x is not r:
                x.warp_to(loc)
        self.remove_property('worn')

    def make_component_of(self, obj):
        assert isinstance(obj, Object), 'The target must be an object.'
        self.set_bulk(0)
        self.add_property('component')
        self.add_property('unlisted')
        obj.add_component(self)
        self.warp_to(obj.get_loc())
        self.parent_object = obj

    def separate_component(self):
        assert 'component' in self.get_properties(), 'The object must be a component.'
        self.get_parent_object().remove_component(self)
        self.remove_property('component')
        self.remove_property('unlisted')
        del self.parent_object

    def get_components(self):
        return self.components

    def add_component(self, obj):
        assert isinstance(obj, Object), 'The component must be an object.'
        if obj not in self.get_components():
            self.get_components().append(obj)

    def remove_component(self, obj):
        assert isinstance(obj, Object), 'The component must be an object.'
        if obj in self.components:
            self.get_components().remove(obj)

    def get_allowed_parent_attachments(self):
        return self.allowed_parent_attachments

    def get_allowed_child_attachments(self):
        return self.allowed_child_attachments

    def get_parent_attachment(self):
        return self.parent_attachment

    def get_child_attachments(self):
        return self.child_attachments

    def set_allowed_parent_attachments(self, l):
        assert type(l) == list, 'The list of allowed parent attachments must be a list.'
        for x in l:
            assert isinstance(x, Object), 'The list of allowed parent attachments must be a list of objects.'
        self.allowed_parent_attachments = l

    def set_allowed_child_attachments(self, l):
        assert type(l) == list, 'The list of allowed child attachments must be a list.'
        for x in l:
            assert isinstance(x, Object), 'The list of allowed child attachments must be a list of objects.'
        self.allowed_child_attachments = l

    def add_allowed_parent_attachment(self, thing):
        assert isinstance(thing, Object), 'The allowed parent attachment must be an object.'
        if thing not in self.allowed_parent_attachments:
            self.allowed_parent_attachments.append(thing)

    def remove_allowed_parent_attachment(self, thing):
        assert isinstance(thing, Object), 'The allowed parent attachment must be an object.'
        if thing in self.allowed_parent_attachments:
            self.allowed_parent_attachments.remove(thing)

    def add_allowed_child_attachment(self, thing):
        assert isinstance(thing, Object), 'The allowed child attachment must be an object.'
        if thing not in self.allowed_parent_attachments:
            self.allowed_child_attachments.append(thing)

    def remove_allowed_child_attachment(self, thing):
        assert isinstance(thing, Object), 'The allowed child attachment must be an object.'
        if thing in self.allowed_child_attachments:
            self.allowed_child_attachments.remove(thing)

    def attach_to(self, thing):
        assert isinstance(thing, Object), 'The parent attachment must be an object.'
        assert thing in self.get_allowed_parent_attachments(), 'The parent attachment must be an allowed parent attachment.'
        assert self in thing.get_allowed_child_attachments(), 'The child attachment must be an allowed child attachment.'
        if hasattr(self, 'parent_attachment'):
            self.detach()
        self.parent_attachment = thing
        thing.child_attachments.append(self)
        self.warp_to(thing.get_loc())

    def detach(self):
        assert hasattr(self, 'parent_attachment'), 'The object must be attached to something.'
        self.get_parent_attachment().get_child_attachments().remove(self)
        del self.parent_attachment

    def get_parent_object(self):
        assert 'component' in self.get_properties(), 'The object must be a component.'
        return self.parent_object

    def add_synonym(self, word):
        assert type(word) == str, 'The synonym must be a string.'
        self.synonyms.append(word)
        noundict[word] = self.id

    def remove_synonym(self, word):
        assert type(word) == str, 'The synonym must be a string.'
        if word in self.synonyms:
            self.synonyms.remove(word)
            if word in noundict:
                del noundict[word]
            elif word in multinoundict:
                l = []
                for x in multinoundict[word]:
                    if x != self.id:
                        l.append(x)
                if len(l) == 2:
                    noundict[word] = tuple(l)
                    multinoundict.pop(word)
                else:
                    multinoundict[word] = tuple(l)

    def get_properties(self):
        return self.properties

    def add_property(self, prop):
        if prop not in self.properties:
            self.get_properties().append(prop)

    def remove_property(self, prop):
        if prop in self.properties:
            self.get_properties().remove(prop)

    def get_name(self):
        return self.name

    def get_loc(self):
        return self.loc

    def find_ultimate_room(self):
        if (isinstance(self.get_loc(), Room)):
            return self.get_loc()
        else:
            return self.get_loc().find_ultimate_room()

    def set_bulk(self, num):
        assert type(num) == int, 'The bulk must be an integer.'
        self.bulk = num

    def get_bulk(self):
        return self.bulk

    def set_custom_immobile_message(self, msg):
        assert type(msg) == str, 'The message must be a string.'
        self.custom_immobile_message = msg

    def get_custom_immobile_message(self):
        return self.custom_immobile_message

    def set_brightness(self, num):
        assert num in [0, 1, 2], 'The brightness value must be 0, 1, or 2.'
        self.brightness = num

    def get_brightness(self):
        return self.brightness

    def is_illuminated(self):
        if self.get_brightness() == 2:
            return True
        elif isinstance(self, Container) and (self.is_transparent() or self.is_open()):
            for x in self.get_contents():
                if x.is_illuminated():
                    return True
        return False

    def is_known(self):
        return self.known

    def make_known(self):
        self.known = True

    def make_unknown(self):
        self.known = False

    def get_remaps_d(self):
        return self.remaps_d

    def get_remaps_i(self):
        return self.remaps_i

    def add_remap_d(self, v, o):
        assert isinstance(v, Verb1) or isinstance(v, Verb2), 'The verb input must be a divalent or trivalent verb.'
        assert isinstance(o, Object), 'The object input must be an object.'
        self.remaps_d[v] = o

    def add_remap_i(self, v, o):
        assert isinstance(v, Verb2), 'The verb input must be a trivalent verb.'
        assert isinstance(o, Object), 'The object input must be an object.'
        self.remaps_i[v] = o

    def remove_remap_d(self, v):
        assert isinstance(v, Verb1) or isinstance(v, Verb2), 'The verb input must be a divalent or trivalent verb.'
        if v in self.remaps_d:
            del self.remaps_d[v]

    def remove_remap_i(self, v):
        assert isinstance(v, Verb2), 'The verb input must be a trivalent verb.'
        if v in self.remaps_i:
            del self.remaps_i[v]

    def art_d(self):
        if self.articles[0] == '':
            return self.get_name()
        else:
            return self.articles[0] + ' ' + self.get_name()

    def art_i(self):
        if self.articles[1] == '':
            return self.get_name()
        else:
            return self.articles[1] + ' ' + self.get_name()

    def is_plural(self):
        return self.plural

    def set_definite_article(self, word):
        assert type(word) == str, 'The article must be a string.'
        self.articles[0] = word

    def set_indefinite_article(self, word):
        assert type(word) == str, 'The article must be a string.'
        self.articles[1] = word

    def make_plural(self):
        if self.articles[1] in ['a', 'an']:
            self.set_indefinite_article('some')
        if self.desc == 'It is an ordinary ' + self.name + '.':
            self.desc = 'They are ordinary ' + self.name + '.'
        self.plural = True
        self.pronoun = self.pluralize(self.pronoun)

    def make_singular(self, newpronoun='it'):
        self.pronoun = newpronoun
        if self.articles[1] == 'some':
            self.set_indefinite_article(self.test_a_an())
        if self.desc == 'These are ordinary ' + self.name + '.':
            self.desc = 'This is an ordinary ' + self.name + '.'
        self.plural = False

    def set_pronoun(self, word):
        assert word in pronouns, 'The word must be a pronoun.'
        self.pronoun = word

    def get_pronoun(self):
        return self.pronoun

    def pluralize(self, phrase):
        if self.is_plural():
            l = phrase.split(' ')
            b = ''
            for word in l:
                if word in pluralsdict:
                    b += pluralsdict[word]; b += ' '
                elif word[-1] == 's':
                    b += word[:-1]; b += ' '
                else:
                    b += word; b += ' '
            return b[:-1]
        else:
            return phrase

    def is_within(self, thing):
        assert isinstance(thing, Room) or isinstance(thing, Object), 'The location to be checked must be a room or an object.'
        if self.get_loc() == thing:
            return True
        elif isinstance(self.get_loc(), Room):
            return False
        else:
            return self.get_loc().is_within(thing)

    def is_reachable(self):
        if 'distant' in self.get_properties():
            return False
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            if self.get_loc() == player or (self.get_loc() == player.get_state_position() or self == player.get_state_position()):
                return True
            elif isinstance(self.get_loc(), Container) and self.get_loc().is_open():
                return self.get_loc().is_reachable()
            else:
                return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and self.get_loc().is_open():
            return self.get_loc().is_reachable()
        else:
            return False

    def is_visible(self):
        if player.get_loc().is_illuminated():
            if 'hidden' in self.get_properties():
                return False
            elif self.get_loc() == player or self.get_loc() == player.get_loc():
                return True
            elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent()):
                return self.get_loc().is_visible()
            else:
                return False
        else:
            if 'hidden' in self.get_properties():
                return False
            elif self.get_loc() == player:
                return True
            elif self.get_loc() == player.get_loc() and self.get_brightness() == 1:
                return True
            elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent()):
                return self.get_loc().is_visible()
            else:
                return False

    def is_audible(self):
        if 'hidden' in self.get_properties():
            return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_sound()):
            return self.get_loc().is_audible()
        else:
            return False

    def is_touchable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            if self.get_loc() == player or (self.get_loc() == player.get_state_position() or self == player.get_state_position()):
                return True
            elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_touch()):
                return self.get_loc().is_touchable()
            else:
                return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_touch()):
            return self.get_loc().is_touchable()
        else:
            return False

    def is_smellable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_smell()):
            return self.get_loc().is_smellable()
        else:
            return False

    def is_tasteable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            if self.get_loc() == player or (self.get_loc() == player.get_state_position() or self == player.get_state_position()):
                return True
            elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_taste()):
                return self.get_loc().is_tasteable()
            else:
                return False
        elif self.get_loc() == player or self.get_loc() == player.get_loc():
            return True
        elif isinstance(self.get_loc(), Container) and (self.get_loc().is_open() or self.get_loc().is_transparent_taste()):
            return self.get_loc().is_tasteable()
        else:
            return False

    def attachment_desc_helper(self):
        if len(self.get_child_attachments()) > 0:
            names = []
            plug_names = []
            tie_names = []
            pluralflag = False
            plug_pluralflag = False
            tie_pluralflag = False
            for x in self.get_child_attachments():
                if 'plug' in x.get_properties():
                    plug_names.append(x.art_i())
                    if x.is_plural():
                        plug_pluralflag = True
                elif isinstance(x, Rope):
                    tie_names.append(x.art_i())
                    if x.is_plural():
                        tie_pluralflag = True
                else:
                    names.append(x.art_i())
                    if x.is_plural():
                        pluralflag = True
            if len(names) > 1 or pluralflag: #some trickery here, if there is one object and it's plural, use 'are' in the description
                pront(f'{sequence(names, "and").capitalize()} are attached to {obliquefy(self.get_pronoun())}.')
            elif len(names) > 0: #possibly zero if all are plugs
                pront(f'{sequence(names, "and").capitalize()} is attached to {obliquefy(self.get_pronoun())}.')
            if len(tie_names) > 1 or tie_pluralflag: #see above comment about trickery
                pront(f'{sequence(tie_names, "and").capitalize()} are tied to {obliquefy(self.get_pronoun())}.')
            elif len(tie_names) > 0: #possibly zero if none are plugs
                pront(f'{sequence(tie_names, "and").capitalize()} is tied to {obliquefy(self.get_pronoun())}.')
            if len(plug_names) > 1 or plug_pluralflag: #see above comment about trickery
                pront(f'{sequence(plug_names, "and").capitalize()} are plugged into {obliquefy(self.get_pronoun())}.')
            elif len(plug_names) > 0: #possibly zero if none are plugs
                pront(f'{sequence(plug_names, "and").capitalize()} is plugged into {obliquefy(self.get_pronoun())}.')

    def describe(self):
        pront(self.desc)
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

    def set_sound_description(self, desc):
        assert type(desc) == str or (isinstance(desc, Perception) or isinstance(desc, PerceptionLink)), 'The description must be a string or a perception or a perception link.'
        self.sound_desc = desc

    def set_smell_description(self, desc):
        assert type(desc) == str or (isinstance(desc, Perception) or isinstance(desc, PerceptionLink)), 'The description must be a string or a perception or a perception link.'
        self.smell_desc = desc

    def set_taste_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.taste_desc = desc

    def set_touch_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.touch_desc = desc

    def set_read_description(self, desc):
        assert type(desc) == str, 'The description must be a string.'
        self.read_desc = desc

    def get_read_description(self):
        return self.read_desc

    def is_noisy(self):
        if isinstance(self, Container):
            if isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
                return True
            else:
                if self.is_transparent_sound() or self.is_open():
                    for x in self.get_contents():
                        if x.is_noisy():
                            return True
        else:
            if isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
                return True
        return False

    def is_smelly(self):
        if isinstance(self, Container):
            if isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
                return True
            else:
                if self.is_transparent_smell() or self.is_open():
                    for x in self.get_contents():
                        if x.is_smelly():
                            return True
        else:
            if isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
                return True
        return False

    def describe_sound(self):

        def report_ambient_sounds(thing):
            if (isinstance(thing, Container) and (thing.is_transparent_sound() or thing.is_open())) or isinstance(thing, Room):
                for x in thing.get_contents():
                    report_ambient_sounds(x)
            if isinstance(thing.sound_desc, Perception) and thing.sound_desc.get_activity():
                if isinstance(thing, Room) or thing.is_visible():
                    pront(thing.sound_desc.get_description())
                else:
                    pront(thing.sound_desc.get_invisible_description())

        def find_outermost_location(thing):
            if (isinstance(thing.get_loc(), Container) and not thing.get_loc().is_transparent_sound()) or isinstance(thing.get_loc(), Room):
                return thing.get_loc()
            else:
                return find_outermost_location(thing.get_loc())

        if isinstance(self.sound_desc, PerceptionLink):
            if self.sound_desc.get_activity():
                destination = self.sound_desc.get_input()
                target = find_outermost_location(destination)
                if isinstance(target, Room):
                    report_ambient_sounds(target)
                elif isinstance(target, Container):
                    report_ambient_sounds(target)
                    for x in target.get_contents():
                        report_ambient_sounds(x)
            else:
                pront(self.smell_desc.get_inactive_sound_description())
        if isinstance(self, Container) and self.is_noisy():
            report_ambient_sounds(self)
        else:
            if isinstance(self.sound_desc, str):
                pront(self.sound_desc)
            elif isinstance(self.sound_desc, Perception) and self.sound_desc.get_activity():
                if self.is_visible():
                    pront(self.sound_desc.get_description())
                else:
                    pront(self.sound_desc.get_invisible_description())

    def describe_smell(self):

        def report_ambient_smells(thing):
            if (isinstance(thing, Container) and (thing.is_transparent_smell() or thing.is_open())) or isinstance(thing, Room):
                for x in thing.get_contents():
                    report_ambient_smells(x)
            if isinstance(thing.smell_desc, Perception) and thing.smell_desc.get_activity():
                if isinstance(thing, Room) or thing.is_visible():
                    pront(thing.smell_desc.get_description())
                else:
                    pront(thing.smell_desc.get_invisible_description())

        def find_outermost_location(thing):
            if (isinstance(thing.get_loc(), Container) and not thing.get_loc().is_transparent_smell()) or isinstance(thing.get_loc(), Room):
                return thing.get_loc()
            else:
                return find_outermost_location(thing.get_loc())

        if isinstance(self.smell_desc, PerceptionLink):
            if self.smell_desc.get_activity():
                destination = self.smell_desc.get_input()
                target = find_outermost_location(destination)
                if isinstance(target, Room):
                    report_ambient_smells(target)
                elif isinstance(target, Container):
                    report_ambient_smells(target)
                    for x in target.get_contents():
                        report_ambient_smells(x)
            else:
                pront(self.smell_desc.get_inactive_smell_description())
        if isinstance(self, Container) and self.is_smelly():
            report_ambient_smells(self)
        else:
            if isinstance(self.smell_desc, str):
                pront(self.smell_desc)
            elif isinstance(self.smell_desc, Perception) and self.smell_desc.get_activity():
                if self.is_visible():
                    pront(self.smell_desc.get_description())
                else:
                    pront(self.smell_desc.get_invisible_description())

    def describe_taste(self):
        pront(self.taste_desc)

    def describe_touch(self):
        pront(self.touch_desc)

    def get_allowed_states(self):
        return []

    def d_o_check(self, v):
        return True

    def i_o_check(self, v, d_o):
        return True

class MultiObject(Object):
    def __init__(self, name, id, synonyms):
        assert type(name) == str, 'The name of the object must be a string.'
        assert type(id) == str, 'The internal id of the object must be a string.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.name = name
        self.id = id
        self.synonyms = synonyms
        for x in self.synonyms:
            if x in noundict:
                multinoundict[x] = (noundict[x], self.id)
                noundict.pop(x)
            elif x in multinoundict:
                temp = multinoundict[x]
                new = temp + (self.id,)
                multinoundict[x] = new
            else:
                noundict[x] = self.id
        noun_id_dict[self.id] = self
        self.desc = 'It is an ordinary ' + self.name + '.'
        self.loc_list = []
        self.properties = []
        self.bulk = 10
        self.brightness = 0
        self.components = []
        self.remaps_d = {}
        self.remaps_i = {}
        self.articles = ['the', test_a_an(self.name)]
        self.plural = False
        self.allowed_parent_attachments = []
        self.allowed_child_attachments = []
        self.child_attachments = []
        self.known = False
        self.custom_immobile_message = 'It cannot be moved.'
        self.pronoun = 'it'
        self.sound_desc = 'You hear nothing.'
        self.smell_desc = 'You smell nothing.'
        self.touch_desc = 'You feel nothing unusual.'
        self.taste_desc = 'You taste no distinct flavor.'
        self.read_desc = 'Nothing is written there.'
        self.add_property('distant')
        self.add_property('immobile')


    def warp_to(self, loc):
        raise Exception('This method (warp_to) should not be used for a MultiObject.')

    def get_loc(self):
        raise Exception('This method (get_loc) should not be used for a MultiObject.')

    def set_loc_list(self, l):
        assert type(l) == list, 'The list of locations must be a list.'
        for x in l:
            assert isinstance(x, Room), 'Only rooms are acceptable locations.'
        self.loc_list = l

    def get_loc_list(self):
        return self.loc_list

    def add_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        if loc not in self.loc_list:
            self.loc_list.append(loc)

    def remove_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        if loc in self.loc_list:
            self.loc_list.remove(loc)

    def is_within(self, thing):
        assert isinstance(thing, Room) or isinstance(thing, Object), 'The location to be checked must be a room or an object.'
        if thing in self.get_loc_list():
            return True
        return False

    def is_reachable(self):
        if 'distant' in self.get_properties():
            return False
        elif (hasattr(player, 'state_position') and player.get_state() != 'standing') and not 'ground' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
            #???? mystery effects
        else:
            return False

    def is_visible(self):
        if player.get_loc().is_illuminated():
            if 'hidden' in self.get_properties():
                return False
            elif player.get_loc() in self.get_loc_list():
                return True
            else:
                return False
        else:
            if 'hidden' in self.get_properties():
                return False
            elif player.get_loc() in self.get_loc_list() and self.get_brightness() == 1:
                return True
            else:
                return False

    def is_audible(self):
        if 'hidden' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
        else:
            return False

    def is_touchable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif (hasattr(player, 'state_position') and player.get_state() != 'standing') and not 'ground' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
        else:
            return False

    def is_smellable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
        else:
            return False

    def is_tasteable(self):
        if 'hidden' in self.get_properties() or 'distant' in self.get_properties():
            return False
        elif (hasattr(player, 'state_position') and player.get_state() != 'standing') and not 'ground' in self.get_properties():
            return False
        elif player.get_loc() in self.get_loc_list():
            return True
        else:
            return False

#all of these are dummy room components (walls, floors, etc.) for the default room types so they player doesn't get messages like "there is no floor here!"
dummy_ground = MultiObject('ground', 'ground#dummy', ['ground', 'floor'])
dummy_ground.remove_property('distant')
dummy_ground.add_property('ground')
dummy_ground.set_indefinite_article('')
dummy_ground.set_description('It is ordinary ground.')
dummy_sky = MultiObject('sky', 'sky#dummy', ['sky'])
dummy_wall = MultiObject('wall', 'wall#dummy', ['wall', 'walls'])
dummy_wall.remove_property('distant')
dummy_floor = MultiObject('floor', 'floor#dummy', ['floor', 'ground'])
dummy_floor.remove_property('distant')
dummy_floor.add_property('ground')
dummy_ceiling = MultiObject('ceiling', 'ceiling#dummy', ['ceiling'])
dummy_ceiling.remove_property('distant')

class InsideRoom(Room):

    def __init__(self):
        super().__init__()
        dummy_wall.add_loc(self)
        dummy_floor.add_loc(self)
        dummy_ceiling.add_loc(self)

class OutsideRoom(Room):

    def __init__(self):
        super().__init__()
        dummy_ground.add_loc(self)
        dummy_sky.add_loc(self)

class Container(Object):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.capacity = 100
        self.contents = []
        self.locked = False
        self.open = True
        self.transparent = False
        self.transparent_sound = False
        self.transparent_touch = False
        self.transparent_smell = False
        self.transparent_taste = False

    def set_capacity(self, num):
        assert type(num) == int, 'The capacity must be an integer.'
        self.capacity = num

    def get_capacity(self):
        return self.capacity

    def get_contents(self):
        return self.contents

    def set_transparent(self, val):
        assert type(val) == bool, 'The transparency must be a boolean.'
        self.transparent = val

    def set_transparent_sound(self, val):
        assert type(val) == bool, 'The sound transparency must be a boolean.'
        self.transparent_sound = val

    def set_transparent_touch(self, val):
        assert type(val) == bool, 'The touch transparency must be a boolean.'
        self.transparent_touch = val

    def set_transparent_smell(self, val):
        assert type(val) == bool, 'The smell transparency must be a boolean.'
        self.transparent_smell = val

    def set_transparent_taste(self, val):
        assert type(val) == bool, 'The sound transparency must be a boolean.'
        self.transparent_taste = val

    def add_content(self, thing):
        assert isinstance(thing, Object), 'The container can only hold other objects.'
        if thing not in self.contents:
            self.get_contents().append(thing)

    def remove_content(self, thing):
        assert isinstance(thing, Object), 'The container can only hold other objects.'
        if thing in self.contents:
            self.get_contents().remove(thing)

    def list_contents(self, n=0):
        if len(self.get_contents()) > 0:
            for x in self.get_contents():
                if 'unlisted' not in x.get_properties() and 'hidden' not in x.get_properties():
                    w = ''
                    if 'plug' in x.get_properties() and isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (plugged into '
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (tied to '
                    if isinstance(x, Rope) and len(x.get_tied_objects()) == 1:
                        w += f' (tied to {x.get_tied_objects()[0].art_d()})'
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) == 2:
                        w += f' (tied to {x.get_tied_objects()[0].art_d()} and {x.get_tied_objects()[1].art_d()})'
                    if hasattr(x, 'parent_attachment'):
                        if 'plug' in x.get_properties():
                            w += f' (plugged into {x.get_parent_attachment().art_d()})'
                        else:
                            w += f' (attached to {x.get_parent_attachment().art_d()})'
                    if 'worn' in x.get_properties():
                        w += ' (being worn)'
                    if 'lamp' in x.get_properties() and x.get_brightness() == 2:
                        w += ' (lit)'
                    pront('  ' * n + x.art_i() + w)
                    if isinstance(x, Surface) and len(x.get_contents()) > 0:
                        pront('  ' * n + f'{x.art_d().capitalize()} {x.pluralize("bears")}:')
                        x.list_contents(n+1)
                    elif isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()):
                        pront('  ' * n + f'{x.art_d().capitalize()} {x.pluralize("contains")}:')
                        x.list_contents(n+1)

    def get_content_bulk(self):
        b = 0
        for x in self.get_contents():
            b += x.get_bulk()
        return b

    def is_open(self):
        return self.open

    def is_locked(self):
        return self.locked

    def is_transparent(self):
        return self.transparent

    def is_transparent_sound(self):
        return self.transparent_sound

    def is_transparent_touch(self):
        return self.transparent_touch

    def is_transparent_smell(self):
        return self.transparent_smell

    def is_transparent_taste(self):
        return self.transparent_taste

    def make_open(self):
        self.open = True
        player.know_objects_in_loc(self)

    def make_closed(self):
        self.open = False

    def describe(self):
        if self.is_open():
            if len(self.get_contents()) > 0:
                pront(self.desc + f' {self.pluralize("It contains")}:')
                self.list_contents()
            else:
                pront(self.desc + f' {self.pluralize("It is")} empty.')
        elif self.is_transparent():
            if len(self.get_contents()) > 0:
                pront(self.desc + f' {self.pluralize("It is")} closed. {self.pluralize("It contains")}:')
                self.list_contents()
            else:
                pront(self.desc + f' {self.pluralize("It is")} closed and empty.')
        else:
            pront(self.desc + f' {self.pluralize("It is")} closed.')
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

    def update_internal_ropes(self):
        for x in self.get_contents():
            if isinstance(x, Rope):
                x.update_locations()
            elif isinstance(x, Container):
                x.update_internal_ropes()

    def check_taut_ropes(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        for x in self.get_contents():
            if isinstance(x, Rope):
                l = x.get_tied_objects()
                if len(l) == 1:
                    if len(x.get_room_order()) >= x.get_max_length() + 1 and not (len(x.get_room_order()) > 1 and loc == x.get_room_order()[-2]):
                        if l[0] in x.get_draggable_objects():
                            place = x.get_room_order()[0]
                            x.set_room_order(x.get_room_order()[1:])
                            if place not in x.get_room_order():
                                x.trail.remove_loc(place)
                            l[0].drag_to(x.get_room_order()[0], x)
                            return False
                        else:
                            pront(f'{x.art_d().capitalize()} jerks you to a stop as you try to leave; you will have to set it down if you want to go further.')
                            return True
                elif len(l) == 2:
                    if len(x.get_room_order()) >= x.get_max_length() + 1 and not (len(x.get_room_order()) > 1 and loc == x.get_room_order()[-2]):
                        if l[0] in self.get_contents():
                            z = l[1]
                        else:
                            z = l[0]
                        if z in x.get_draggable_objects():
                            place = x.get_room_order()[0]
                            x.set_room_order(x.get_room_order()[1:])
                            if place not in x.get_room_order():
                                x.trail.remove_loc(place)
                            z.drag_to(x.get_room_order()[0], x)
                            return False
                        else:
                            pront(f'{x.art_d().capitalize()} jerks you to a stop as you try to leave; you will have to set it down if you want to go further.')
                            return True
                return False
            elif isinstance(x, Container):
                if x.check_taut_ropes(loc):
                    return True
        return False

    def warp_to(self, loc):
        super().warp_to(loc)
        self.update_internal_ropes()

class Surface(Container):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)

    def describe(self):
        if len(self.get_contents()) > 1 or (len(self.get_contents()) == 1 and self.get_contents()[0].is_plural()):
            pront(self.desc + f' On {obliquefy(self.pluralize("it"))} are:')
            self.list_contents()
        elif len(self.get_contents()) == 1:
            pront(self.desc + f' On {obliquefy(self.pluralize("it"))} is:')
            self.list_contents()
        else:
            pront(self.desc)
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

class Furniture(Surface):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['sitting']
        self.default_state = 'sitting'
        self.add_property('immobile')

    def get_allowed_states(self):
        return self.allowed_states

    def set_allowed_states(self, l):
        assert type(l) == list, 'The allowed states must be in a list.'
        for x in l:
            assert type(x) == str, 'The allowed states must all be strings.'
        self.allowed_states = l

    def add_allowed_state(self, s):
        assert type(s) == str, 'The allowed state must be a string.'
        if s not in self.allowed_states:
            self.allowed_states.append(s)

    def remove_allowed_state(self, s):
        assert type(s) == str, 'The allowed state must be a string.'
        if s in self.allowed_states:
            self.allowed_states.remove(s)

    def get_default_state(self):
        return self.default_state

    def set_default_state(self, s):
        assert type(s) == str, 'The default state must be a string.'
        self.default_state = s

class Vehicle(Object):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['riding a vehicle']
        self.default_state = 'riding a vehicle'
        self.add_property('immobile')

    def get_allowed_states(self):
        return self.allowed_states

    def set_allowed_states(self, l):
        assert type(l) == list, 'The allowed states must be in a list.'
        for x in l:
            assert type(x) == str, 'The allowed states must all be strings.'
        self.allowed_states = l

    def add_allowed_state(self, s):
        assert type(s) == str, 'The allowed state must be a string.'
        if s not in self.allowed_states:
            self.allowed_states.append(s)

    def remove_allowed_state(self, s):
        assert type(s) == str, 'The allowed state must be a string.'
        if s in self.allowed_states:
            self.allowed_states.remove(s)

    def get_default_state(self):
        return self.default_state

    def set_default_state(self, s):
        assert type(s) == str, 'The default state must be a string.'
        self.default_state = s

class Chair(Furniture):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['sitting', 'standing atop something']
        self.default_state = 'sitting'

class Bed(Furniture):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['lying down', 'sitting', 'standing atop something']
        self.default_state = 'lying down'

class Table(Furniture):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['standing atop something', 'sitting']
        self.default_state = 'standing atop something'

class Mat(Furniture):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.allowed_states = ['standing', 'sitting', 'lying down']
        self.default_state = 'standing'

class Wrapper(Container):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.open = False
        self.locked = False
        self.add_property('openable')

    def make_open(self):
        super().make_open()
        self.remove_property('openable')

class Locker(Container):

    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.open = False
        self.locked = True
        self.keylist = []
        self.add_property('openable')

    def get_keylist(self):
        return self.keylist

    def add_key(self, key):
        assert isinstance(key, Object), 'The key must be an object.'
        if key not in self.keylist:
            self.keylist.append(key)

    def remove_key(self, key):
        assert isinstance(key, Object), 'The key must be an object.'
        if key in self.keylist:
            self.keylist.remove(key)

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

class Ampuole(Locker):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.open = False
        self.locked = True
        self.keylist = []

    def make_open(self):
        super().make_open()
        self.remove_property('openable')

class Ladder(Object):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.up_destination = offstage
        self.down_destination = offstage
        self.valid_up = False
        self.valid_down = False
        self.move_up_message = f'You climb up {self.art_d()}.'
        self.move_down_message = f'You climb down {self.art_d()}.'
        self.add_property('immobile')
        self.add_property('unlisted')

    def set_valid_up(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.valid_up = val

    def leads_up(self):
        return self.valid_up

    def set_valid_down(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.valid_down = val

    def leads_down(self):
        return self.valid_down

    def set_up_destination(self, loc):
        assert isinstance(loc, Room), 'The destination must be a room.'
        self.up_destination = loc

    def get_up_destination(self):
        return self.up_destination

    def set_down_destination(self, loc):
        assert isinstance(loc, Room), 'The destination must be a room.'
        self.down_destination = loc

    def get_down_destination(self):
        return self.down_destination

    def get_move_up_message(self):
        return self.move_up_message

    def set_move_up_message(self, msg):
        assert type(msg) == str, 'The movement message must be a string.'
        self.move_up_message = msg

    def get_move_down_message(self):
        return self.move_down_message

    def set_move_down_message(self, msg):
        assert type(msg) == str, 'The movement message must be a string.'
        self.move_down_message = msg

class Door(Object):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.locked = False
        self.open = False
        self.locklink = True
        self.connection = self
        self.move_message = f'You go into {self.art_d()}.'
        self.add_property('immobile')
        self.add_property('openable')
        self.add_property('unlisted')
        self.add_property('portal')

    def is_open(self):
        return self.open

    def is_locked(self):
        return self.locked

    def make_open(self):
        self.open = True
        self.get_connection().open = True

    def make_closed(self):
        self.open = False
        self.get_connection().open = False

    def set_connection(self, other):
        assert isinstance(other, Door), 'Doors can only connect to doors.'
        self.connection = other
        other.connection = self

    def get_connection(self):
        return self.connection

    def link_locks(self):
        self.locklink = True

    def unlink_locks(self):
        self.locklink = False

    def get_locklink(self):
        return self.locklink

    def get_move_message(self):
        return self.move_message

    def set_move_message(self, msg):
        assert type(msg) == str, 'The movement message must be a string.'
        self.move_message = msg

    def describe(self):
        if self.is_open() and 'openable' in self.get_properties():
            pront(self.desc + f' {self.pluralize("It is")} currently open.')
        elif 'openable' in self.get_properties():
            pront(self.desc + f' {self.pluralize("It is")} currently closed.')
        else:
            pront(self.desc)
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

class LockedDoor(Door):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.locked = True

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

class KeyedDoor(LockedDoor):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.keylist = []

    def get_keylist(self):
        return self.keylist

    def add_key(self, key):
        assert isinstance(key, Object), 'The key must be an object.'
        if key not in self.keylist:
            self.keylist.append(key)

    def remove_key(self, key):
        assert isinstance(key, Object), 'The key must be an object.'
        if key in self.keylist:
            self.keylist.remove(key)

class RopeTrail(MultiObject):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.remove_property('distant')
        self.remove_property('immobile')
        self.add_property('unlisted')

    def is_visible(self):
        if self.parent_rope.is_visible() or len(self.parent_rope.get_tied_objects()) == 0:
            return False
        else:
            return super().is_visible()

    def describe(self):
        pront(self.parent_rope.desc)

    def set_loc_list(self, l):
        assert type(l) == list, 'The list of locations must be a list.'
        for x in l:
            assert isinstance(x, Room), 'Only rooms are acceptable locations.'
        ll = self.loc_list.copy()
        for y in ll:
            self.loc_list.remove(y)
            y.contents.remove(self)
        for z in l:
            self.add_loc(z)

    def get_loc_list(self):
        return self.loc_list

    def add_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        if loc not in self.loc_list:
            self.loc_list.append(loc)
            loc.contents.append(self)

    def remove_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        if loc in self.loc_list:
            self.loc_list.remove(loc)
            loc.contents.remove(self)

    def get_parent_rope(self):
        return self.parent_rope

class Rope(Object):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.trail = RopeTrail(self.name, self.id + '#trail', self.synonyms)
        self.trail.parent_rope = self
        self.room_order = [offstage]
        self.max_length = 0
        self.tied_objects = []
        self.draggable_objects = []

    def get_max_length(self):
        return self.max_length

    def set_max_length(self, n):
        assert type(n) == int and n > 0, 'The maximum length must be a positive integer.'
        self.max_length = n

    def get_room_order(self):
        return self.room_order

    def set_room_order(self, l):
        assert type(l) == list, 'The room order must be a list.'
        for x in l:
            assert isinstance(x, Room), 'Each room in the list must be a room.'
        self.room_order = l

    def add_room(self, r):
        assert isinstance(r, Room), 'The room must be a room.'
        self.room_order.append(r)

    def get_tied_objects(self):
        return self.tied_objects

    def add_tied_object(self, thing):
        assert isinstance(thing, Object), 'The tied object must be an object.'
        self.tied_objects.append(thing)

    def remove_tied_object(self, thing):
        assert isinstance(thing, Object), 'The tied object must be an object.'
        self.tied_objects.remove(thing)

    def set_tied_objects(self, l):
        assert type(l) == list, 'The list of draggable objects must be a list.'
        for x in l:
            assert isinstance(x, Object), 'Each tied object must be an object.'
        self.tied_objects = l

    def get_draggable_objects(self):
        return self.draggable_objects

    def set_draggable_objects(self, l):
        assert type(l) == list, 'The list of draggable objects must be a list.'
        for x in l:
            assert isinstance(x, Object), 'Each draggable object must be an object.'
        self.draggable_objects = l

    def add_draggable_object(self, thing):
        assert isinstance(thing, Object), 'The draggable object must be an object.'
        self.draggable_objects.append(thing)

    def remove_draggable_object(self, thing):
        assert isinstance(thing, Object), 'The draggable object must be an object.'
        self.draggable_objects.remove(thing)

    def tie_to(self, thing):
        assert isinstance(thing, Object), 'The tied object must be an object.'
        thing.child_attachments.append(self)
        self.add_tied_object(thing)
        if len(self.get_tied_objects()) == 2 and not thing.is_within(player):
            self.warp_to(thing.get_loc())

    def untie_from(self, thing):
        assert isinstance(thing, Object), 'The untied object must be an object.'
        thing.child_attachments.remove(self)
        self.remove_tied_object(thing)
        if len(self.get_tied_objects()) == 0:
            self.warp_to(thing.get_loc())

    def reverse_polarity(self):
        self.set_room_order(self.get_room_order()[::-1])
        self.set_tied_objects(self.get_tied_objects()[::-1])
        #if not self.get_room_order().count(self.get_room_order()[-1]) > 1:
            #self.trail.remove_loc(self.get_room_order()[-1])
        #self.trail.add_loc(self.get_room_order()[0])

    def update_locations(self):
        swapping = False
        if self.is_within(self.get_room_order()[0]) and len(self.get_room_order()) > 1:
            swapping = True
        if swapping or not self.is_within(self.get_room_order()[-1]):
            if len(self.get_tied_objects()) == 0:
                self.set_room_order([self.find_ultimate_room()])
            elif len(self.get_tied_objects()) == 1 and self.get_tied_objects()[0].find_ultimate_room() is self.find_ultimate_room():
                self.set_room_order([self.find_ultimate_room()])
            elif len(self.get_tied_objects()) == 2 and self.get_tied_objects()[0].find_ultimate_room() is self.find_ultimate_room() and self.get_tied_objects()[1].find_ultimate_room() is self.find_ultimate_room():
                self.set_room_order([self.find_ultimate_room()])
            else:
                if len(self.get_room_order()) > 1 and self.is_within(self.get_room_order()[-2]):
                    self.set_room_order(self.get_room_order()[0:-1])
                elif not swapping:
                    self.get_room_order().append(self.find_ultimate_room())

        if swapping:
            self.reverse_polarity()
        self.trail.set_loc_list(self.get_room_order())

    def warp_to(self, loc):
        super().warp_to(loc)
        self.update_locations()

class Player(Container):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.wearing = []
        self.prior_loc = offstage
        self.state = 'standing'
        self.pronoun = 'you'

    def list_contents(self, n=0):
        if len(self.get_contents()) > 0:
            for x in self.get_contents():
                if ('unlisted' not in x.get_properties()) and ('player_anatomy' not in x.get_properties()):
                    w = ''
                    if 'plug' in x.get_properties() and isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (plugged into '
                        if len(x.get_tied_objects()) == 1:
                            w += f'{x.get_tied_objects()[0].art_d()})'
                        elif len(x.get_tied_objects()) == 2:
                            w += f'{x.get_tied_objects()[0].art_d()} and {x.get_tied_objects()[1].art_d()})'
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (tied to '
                        if len(x.get_tied_objects()) == 1:
                            w += f'{x.get_tied_objects()[0].art_d()})'
                        elif len(k.get_tied_objects()) == 2:
                            w += f'{x.get_tied_objects()[0].art_d()} and {x.get_tied_objects()[1].art_d()})'
                    #if isinstance(x, Rope) and len(x.get_tied_objects()) == 1:
                        #w += f' (tied to 3{x.get_tied_objects()[0].art_d()})'
                    #elif isinstance(x, Rope) and len(x.get_tied_objects()) == 2:
                        #w += f' (tied to 4{x.get_tied_objects()[0].art_d()} and {x.get_tied_objects()[1].art_d()})'
                    if hasattr(x, 'parent_attachment'):
                        if 'plug' in x.get_properties():
                            w += f' (plugged into {x.get_parent_attachment().art_d()})'
                        else:
                            w += f' (attached to {x.get_parent_attachment().art_d()})'
                    if 'worn' in x.get_properties():
                        w += ' (being worn)'
                    if 'lamp' in x.get_properties() and x.get_brightness() == 2:
                        w += ' (lit)'
                    pront('  ' * n + x.art_i() + w)
                    if isinstance(x, Surface) and len(x.get_contents()) > 0:
                        pront('  ' * n + f'{x.art_d().capitalize()} {self.pluralize("bears")}:')
                        x.list_contents(n+1)
                    elif isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()):
                        pront('  ' * n + f'{x.art_d().capitalize()} {self.pluralize("contains")}:')
                        x.list_contents(n+1)

    def get_carried(self):
        l = []
        for x in self.get_contents():
            if not 'player_anatomy' in x.get_properties():
                l.append(x)
        return l

    def describe(self):
        pront(self.desc)
        self.attachment_desc_helper()

    def warp_to(self, loc):
        super().warp_to(loc)
        self.know_objects_in_loc(self.get_loc())

    def know_objects_in_loc(self, loc):
        assert isinstance(loc, Room) or isinstance(loc, Object), 'The location to be checked must be a room or an object.'
        if isinstance(loc, Room):
            for x in loc.get_contents():
                if x.is_visible():
                    self.know_objects_in_loc(x)
        elif isinstance(loc, Container) and loc.is_visible():
            loc.make_known()
            for x in loc.get_contents():
                if x.is_visible():
                    self.know_objects_in_loc(x)
        else:
            if loc.is_visible():
                loc.make_known()

    def get_prior_loc(self):
        return self.prior_loc

    def set_prior_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        self.prior_loc = loc

    def get_state(self):
        return self.state

    def set_state(self, s):
        assert type(s) == str, 'The state must be a string.'
        self.state = s

    def reset_state(self):
        if hasattr(self, 'state_position'):
            del self.state_position
        self.state = 'standing'

    def get_state_position(self):
        return self.state_position

    def set_state_position(self, thing):
        assert isinstance(thing, (Furniture, Vehicle)), 'The state position must be an article of furniture or a vehicle.'
        self.state_position = thing

player = Player('yourself','player', ['me', 'myself', 'self'])

class NPC(Container):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.add_property('unlisted')
        self.activity_desc = 'is standing here, doing nothing much in particular.'
        self.wearing = []
        self.covets = []
        self.owngreetingPulser = GreetingPulser(self)
        self.ownwanderPulser = WanderPulser(self)
        self.ownfollowPulser = FollowPulser(self)
        self.room_list = []
        self.private_room_list = []
        self.pronoun = 'they'
        self.greet_msg = 'Hello.'
        self.prior_loc = offstage
        self.greet_dur = 15
        self.last_greet_turn = -2147483648 #farthest negative turn so that NPCs greet player immediately (negative integer limit)
        self.unknown_ask_msg = 'I don\'t know anything about that subject.'
        self.unknown_tell_msg = 'I\'m not sure what to do with that information.'
        self.unknown_show_msg = 'I\'m not sure what to make of that.'
        self.ask_responses = {}
        self.tell_responses = {}
        self.show_responses = {}
        self.ask_event_triggers = []
        self.tell_event_triggers = []
        self.show_event_triggers = []

    def list_contents(self, n=0):
        if len(self.get_contents()) > 0:
            for x in self.get_contents():
                if ('unlisted' not in x.get_properties() and 'hidden' not in x.get_properties()):
                    w = ''
                    if 'plug' in x.get_properties() and isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (plugged into '
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) > 0:
                        w += f' (tied to '
                    if isinstance(x, Rope) and len(x.get_tied_objects()) == 1:
                        w += f' (tied to {x.get_tied_objects()[0].art_d()})'
                    elif isinstance(x, Rope) and len(x.get_tied_objects()) == 2:
                        w += f' (tied to {x.get_tied_objects()[0].art_d()} and {x.get_tied_objects()[1].art_d()})'
                    if hasattr(x, 'parent_attachment'):
                        if 'plug' in x.get_properties():
                            w += f' (plugged into {x.get_parent_attachment().art_d()})'
                        else:
                            w += f' (attached to {x.get_parent_attachment().art_d()})'
                    if 'worn' in x.get_properties():
                        w += ' (being worn)'
                    if 'lamp' in x.get_properties() and x.get_brightness() == 2:
                        w += ' (lit)'
                    pront('  ' * n + x.art_i() + w)
                    if isinstance(x, Surface) and len(x.get_contents()) > 0:
                        pront('  ' * n + f'{x.art_d().capitalize()} {self.pluralize("bears")}:')
                        x.list_contents(n+1)
                    elif isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()):
                        pront('  ' * n + f'{x.art_d().capitalize()} {self.pluralize("contains")}:')
                        x.list_contents(n+1)

    def verify_not_all_hidden(self):
        for x in self.get_contents():
            if 'hidden' not in x.get_properties():
                return True
        return False

    def set_covets(self, l):
        assert type(l) == list, 'The coveted objects must be in a list.'
        for x in l:
            assert isinstance(x, Object), 'All coveted objects must be objects.'
        self.covets = l

    def get_covets(self):
        return self.covets

    def add_coveted(self, thing):
        assert isinstance(thing, Object), 'Only objects can be coveted.'
        if thing not in self.get_covets():
            self.covets.append(thing)

    def remove_coveted(self, thing):
        assert isinstance(thing, Object), 'Only objects can have their coveted status removed.'
        if thing in self.get_covets():
            self.covets.remove(thing)

    def set_room_list(self, l):
        assert type(l) == list, 'The permitted rooms must be in a list.'
        for x in l:
            assert isinstance(x, Room), 'Everything in the room list must be a room.'
        self.room_list = l

    def get_room_list(self):
        return self.room_list

    def add_room(self, thing):
        assert isinstance(thing, Room), 'Only rooms can be added to the room list.'
        if thing not in self.get_room_list():
            self.room_list.append(thing)

    def remove_room(self, thing):
        assert isinstance(thing, Room), 'Only rooms can be removed from the room list.'
        if thing in self.get_room_list():
            self.room_list.remove(thing)

    def set_private_list(self, l):
        assert type(l) == list, 'The private rooms must be in a list.'
        for x in l:
            assert isinstance(x, Room), 'Everything in the private room list must be a room.'
        self.private_room_list = l

    def get_private_list(self):
        return self.private_room_list

    def add_private_room(self, thing):
        assert isinstance(thing, Room), 'Only rooms can be added to the private room list.'
        if thing not in self.get_private_list():
            self.room_list.append(thing)

    def remove_private_room(self, thing):
        assert isinstance(thing, Room), 'Only rooms can be removed from the private room list.'
        if thing in self.get_private_list():
            self.room_list.remove(thing)

    def get_unknown_ask_msg(self):
        return self.unknown_ask_msg

    def set_unknown_ask_msg(self, msg):
        assert isinstance(msg, str), 'The message must be a string.'
        self.unknown_ask_msg = msg

    def get_unknown_tell_msg(self):
        return self.unknown_tell_msg

    def set_unknown_tell_msg(self, msg):
        assert isinstance(msg, str), 'The message must be a string.'
        self.unknown_tell_msg = msg

    def get_unknown_show_msg(self):
        return self.unknown_show_msg

    def set_unknown_show_msg(self, msg):
        assert isinstance(msg, str), 'The message must be a string.'
        self.unknown_show_msg = msg

    def get_ask_responses(self):
        return self.ask_responses

    def set_ask_responses(self, responses):
        assert isinstance(responses, dict), 'The dictionary of responses must be a dictionary.'
        for x in responses:
            assert isinstance(x, Object), 'The keys must all be objects.'
            assert isinstance(responses[x], tuple), 'The values must all be tuples.'
            assert isinstance(responses[x][0], str), 'Each response must be a string.'
            assert isinstance(responses[x][1], bool), 'Each quotation determiner must be a boolean.'
            assert isinstance(responses[x][2], tuple), 'Each collection of learned objects must be a tuple.'
            for y in responses[x][2]:
                assert isinstance(y, Object), 'Each learned object must be an object.'
        self.ask_responses = responses

    def add_ask_response(self, target, response, quotes = True, learned_objects = ()):
        assert isinstance(target, Object), 'The dictionary key must be an object.'
        assert isinstance(response, str), 'The dictionary value must be a string.'
        assert isinstance(quotes, bool), 'The quotation determiner must be a boolean.'
        assert isinstance(learned_objects, tuple), 'The collection of learned objects must be a tuple.'
        for x in learned_objects:
            assert isinstance(x, Object), 'Each learned object must be an object.'
        self.ask_responses[target] = (response, quotes, learned_objects)

    def get_tell_responses(self):
        return self.tell_responses

    def set_tell_responses(self, responses):
        assert isinstance(responses, dict), 'The dictionary of responses must be a dictionary.'
        for x in responses:
            assert isinstance(x, Object), 'The keys must all be objects.'
            assert isinstance(responses[x], tuple), 'The values must all be tuples.'
            assert isinstance(responses[x][0], str), 'Each response must be a string.'
            assert isinstance(responses[x][1], bool), 'Each quotation determiner must be a boolean.'
            assert isinstance(responses[x][2], tuple), 'Each collection of learned objects must be a tuple.'
            for y in responses[x][2]:
                assert isinstance(y, Object), 'Each learned object must be an object.'
        self.tell_responses = responses

    def add_tell_response(self, target, response, quotes = True, learned_objects = ()):
        assert isinstance(target, Object), 'The dictionary key must be an object.'
        assert isinstance(response, str), 'The dictionary value must be a string.'
        assert isinstance(quotes, bool), 'The quotation determiner must be a boolean.'
        assert isinstance(learned_objects, tuple), 'The collection of learned objects must be a tuple.'
        for x in learned_objects:
            assert isinstance(x, Object), 'Each learned object must be an object.'
        self.tell_responses[target] = (response, quotes, learned_objects)

    def get_show_responses(self):
        return self.show_responses

    def set_show_responses(self, responses):
        assert isinstance(responses, dict), 'The dictionary of responses must be a dictionary.'
        for x in responses:
            assert isinstance(x, Object), 'The keys must all be objects.'
            assert isinstance(responses[x], tuple), 'The values must all be tuples.'
            assert isinstance(responses[x][0], str), 'Each response must be a string.'
            assert isinstance(responses[x][1], bool), 'Each quotation determiner must be a boolean.'
            assert isinstance(responses[x][2], tuple), 'Each collection of learned objects must be a tuple.'
            for y in responses[x][2]:
                assert isinstance(y, Object), 'Each learned object must be an object.'
        self.show_responses = responses

    def add_show_response(self, target, response, quotes = True, learned_objects = ()):
        assert isinstance(target, Object), 'The dictionary key must be an object.'
        assert isinstance(response, str), 'The dictionary value must be a string.'
        assert isinstance(quotes, bool), 'The quotation determiner must be a boolean.'
        assert isinstance(learned_objects, tuple), 'The collection of learned objects must be a tuple.'
        for x in learned_objects:
            assert isinstance(x, Object), 'Each learned object must be an object.'
        self.show_responses[target] = (response, quotes, learned_objects)

    def get_ask_event_triggers(self):
        return self.ask_event_triggers

    def set_ask_event_triggers(self, triggers):
        assert isinstance(triggers, list), 'The event triggers must be in a list.'
        for x in triggers:
            assert isinstance(x, Object), 'The event triggers must all be objects.'
        self.ask_event_triggers = triggers

    def add_ask_event_trigger(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'
        if trigger not in self.get_ask_event_triggers():
            self.ask_event_triggers.append(trigger)

    def get_tell_event_triggers(self):
        return self.tell_event_triggers

    def set_tell_event_triggers(self, triggers):
        assert isinstance(triggers, list), 'The event triggers must be in a list.'
        for x in triggers:
            assert isinstance(x, Object), 'The event triggers must all be objects.'
        self.tell_event_triggers = triggers

    def add_tell_event_trigger(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'
        if trigger not in self.get_tell_event_triggers():
            self.tell_event_triggers.append(trigger)

    def get_show_event_triggers(self):
        return self.show_event_triggers

    def set_show_event_triggers(self, triggers):
        assert isinstance(triggers, list), 'The event triggers must be in a list.'
        for x in triggers:
            assert isinstance(x, Object), 'The event triggers must all be objects.'
        self.show_event_triggers = triggers

    def add_show_event_trigger(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'
        if trigger not in self.get_show_event_triggers():
            self.show_event_triggers.append(trigger)

    def do_ask_event(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'

    def do_tell_event(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'

    def do_show_event(self, trigger):
        assert isinstance(trigger, Object), 'The trigger must be an object.'

    def acquire(self, thing):
        assert isinstance(thing, Object), 'Only objects can be acquired.'
        thing.warp_to(self)

    def acquire_and_hide(self, thing):
        assert isinstance(thing, Object), 'Only objects can be acquired and hidden.'
        thing.warp_to(self)
        thing.add_property('hidden')

    def hide(self, thing):
        assert isinstance(thing, Object) and thing.get_loc() == self, 'NPCs can only hide something if it is an object they are currently holding.'
        thing.add_property('hidden')

    def reveal(self, thing):
        assert isinstance(thing, Object) and thing.get_loc() == self, 'NPCs can only reveal something if it is an object they are currently holding.'
        thing.remove_property('hidden')

    def drop(self, thing):
        assert isinstance(thing, Object) and thing.get_loc() == self, 'NPCs can only drop something if it is an object they are currently holding.'
        thing.remove_property('hidden')
        thing.warp_to(self.get_loc())

    def describe(self):
        if len(self.get_contents()) > 0 and self.verify_not_all_hidden():
            pront(self.desc + f' {self.get_pronoun().capitalize()} {self.is_are()} holding:')
            self.list_contents()
        else:
            pront(self.desc)
        self.attachment_desc_helper()
        if self.is_noisy():
            self.describe_sound()
        if self.is_smelly():
            self.describe_smell()

    def set_activity_desc(self, d):
        assert type(d) == str, 'The activity description must be a string.'
        self.activity_desc = d

    def get_activity_desc(self):
        return self.art_i().capitalize() + ' ' + self.activity_desc

    def follow_player(self):
        self.ownwanderPulser.deactivate() #do not wander if following the player
        self.ownfollowPulser.set_dur(0)
        self.ownfollowPulser.activate()

    def stop_following_player(self):
        self.ownfollowPulser.deactivate()
        if self.owngreetingPulser.get_activity():
            self.owngreetingPulser.reactivate()
            self.set_last_greet_turn(MasterState.turn_count)

    def wander(self, dur):
        assert type(dur) == int, 'The duration must be an integer.'
        self.ownfollowPulser.deactivate() #do not follow the player if wandering
        self.ownwanderPulser.activate()
        self.ownwanderPulser.set_dur(dur)

    def stop_wandering(self):
        self.ownwanderPulser.deactivate()

    def greet(self, dur):
        assert type(dur) == int, 'The duration must be an integer.'
        self.owngreetingPulser.activate()
        self.owngreetingPulser.set_dur(0)
        self.greet_dur = dur

    def get_greet_dur(self):
        return self.greet_dur

    def stop_greeting(self):
        self.owngreetingPulser.deactivate()

    def set_greet_msg(self, msg):
        assert type(msg) == str, 'The greeting message must be a string.'
        self.greet_msg = msg

    def get_greet_msg(self):
        return self.greet_msg

    def set_last_greet_turn(self, n):
        assert type(n) == int, 'The turn number must be an integer.'
        self.last_greet_turn = n

    def get_last_greet_turn(self):
        return self.last_greet_turn

    def greet_player(self):
        pront(f'{self.art_d()} says \"{self.get_greet_msg()}\"')

    def set_prior_loc(self, loc):
        assert isinstance(loc, Room), 'The location must be a room.'
        self.prior_loc = loc

    def get_prior_loc(self, loc):
        return self.prior_loc

    def is_are(self):
        if self.get_pronoun() == 'they':
            return 'are'
        return 'is'

    def describe_taste(self):
        pront(f'{self.art_d().capitalize()} would definitely object to that.')

    def describe_touch(self):
        pront(f'{self.art_d().capitalize()} looks at you with a look of annoyance.')

def define_again_verbs(l):
    assert type(l) == list, 'The list of verbs must be a list.'
    for x in l:
        assert isinstance(x, str), 'Only strings are acceptable verb synonyms.'
    for x in l:
        verb0dict[x] = 'again'

class Verb0:

    def __init__(self, id, synonyms):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.id = id
        self.synonyms = synonyms
        for x in synonyms:
            verb0dict[x] = self.id
        verb_id_dict[self.id] = self
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb0dict[word] = self.id

    def execute(self):
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            self.body()
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self):
        pass

    def prioritize(self, thing): #template purposes, should not really be called
        return (thing, 0)

class Verb1:

    def __init__(self, id, synonyms):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.id = id
        self.synonyms = synonyms
        for x in synonyms:
            verb1dict[x] = self.id
        verb_id_dict[self.id] = self
        self.requires_sight = True
        self.requires_contact = True
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_requires_sight(self):
        return self.requires_sight

    def set_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.requires_sight = val

    def get_requires_contact(self):
        return self.requires_contact

    def set_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb1dict[word] = self.id

    def disambiguate(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + self.id.replace('|', ' ') + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    return(f'#You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + self.id.replace('|', ' ') + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize(x))
        return self.infer_nouns(prioritized_thinglist)

    def prioritize(self, thing):
        return (thing, 0)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        return new

    def execute(self, d_o):
        if self in d_o.get_remaps_d():
            d_o = d_o.get_remaps_d()[self]
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            if d_o.d_o_check(self):
                self.body(d_o)
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self, d_o):
        pass

class VerbLit:

    def __init__(self, id, synonyms):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        self.id = id
        self.synonyms = synonyms
        for x in synonyms:
            verblitdict[x] = self.id
        verb_id_dict[self.id] = self
        self.requires_sight = False
        self.requires_contact = False
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_requires_sight(self):
        return self.requires_sight

    def set_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.requires_sight = val

    def get_requires_contact(self):
        return self.requires_contact

    def set_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb1dict[word] = self.id

    def no_vis_notice(self, thing):
        assert isinstance(thing, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id.replace('|', ' ') + ' the ' + thing.get_name() + ' because there is no ' + thing.get_name() + ' here.')

    def disambiguate(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        return potentials.replace('_', ' ')

    def execute(self, d_o):
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            self.body(d_o)
        else:
            pront(f'You cannot do that while {player.get_state()}')

    def body(self, d_o):
        pass

class Verb2:

    def __init__(self, id, synonyms, prepositions):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        assert type(prepositions) == tuple, 'The prepositions must be in a tuple.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        for x in prepositions:
            assert type(x) == str, 'All prepositions must be strings.'
        self.id = id
        self.synonyms = synonyms
        self.prepositions = prepositions
        for x in synonyms:
            verb2dict[x] = (self.id, self.prepositions)
        verb_id_dict[self.id] = self
        self.d_o_requires_sight = True
        self.d_o_requires_contact = True
        self.i_o_requires_sight = True
        self.i_o_requires_contact = True
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_d_o_requires_sight(self):
        return self.d_o_requires_sight

    def set_d_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_sight = val

    def get_d_o_requires_contact(self):
        return self.d_o_requires_contact

    def set_d_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_contact = val

    def get_i_o_requires_sight(self):
        return self.i_o_requires_sight

    def set_i_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_sight = val

    def get_i_o_requires_contact(self):
        return self.i_o_requires_contact

    def set_i_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb2dict[word] = (self.id, self.prepositions)

    def no_vis_notice1(self, thing):
        assert isinstance(thing, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing.art_d()} ' + f' because there is no {thing.art_d()} here.')

    def no_vis_notice2(self, thing1, thing2):
        assert isinstance(thing1, Object), 'Only objects can have visibility checked.'
        assert isinstance(thing2, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + ' ' + thing1.art_d() + ' ' + self.id[self.id.index('_') + 1:].replace('|', ' ') + ' the ' + thing2.get_name() + ' because there is no ' + thing2.get_name() + ' here.')

    def disambiguate_d_o(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_d_o_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_d_o_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    pront(f'You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize_d_o(x))
        return self.infer_nouns(prioritized_thinglist)

    def disambiguate_i_o(self, d_o, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_i_o_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + d_o.get_name() + ' ' + after_(self.id.replace('|', ' ')) + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_i_o_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    return(f'#You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + d_o.get_name() + ' ' + after_(self.id.replace('|', ' ')) + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize_i_o(d_o, x))
        return self.infer_nouns(prioritized_thinglist)

    def prioritize_d_o(self, thing):
        return (thing, 0)

    def prioritize_i_o(self, thing1, thing2):
        return (thing2, 0)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        return new

    def execute(self, d_o, i_o):
        if self in d_o.get_remaps_d():
            d_o = d_o.get_remaps_d()[self]
        if self in i_o.get_remaps_i():
            i_o = i_o.get_remaps_i()[self]
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            if d_o.d_o_check(self):
                if i_o.i_o_check(self, d_o):
                    self.body(d_o, i_o)
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self, d_o, i_o):
        pass

class VerbLit2:

    def __init__(self, id, synonyms, prepositions):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        assert type(prepositions) == tuple, 'The prepositions must be in a tuple.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        for x in prepositions:
            assert type(x) == str, 'All prepositions must be strings.'
        self.id = id
        self.synonyms = synonyms
        self.prepositions = prepositions
        for x in synonyms:
            verblit2dict[x] = (self.id, self.prepositions)
        verb_id_dict[self.id] = self
        self.d_o_requires_sight = True
        self.d_o_requires_contact = True
        self.i_o_requires_sight = True
        self.i_o_requires_contact = True
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_d_o_requires_sight(self):
        return self.d_o_requires_sight

    def set_d_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_sight = val

    def get_d_o_requires_contact(self):
        return self.d_o_requires_contact

    def set_d_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_contact = val

    def get_i_o_requires_sight(self):
        return self.i_o_requires_sight

    def set_i_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_sight = val

    def get_i_o_requires_contact(self):
        return self.i_o_requires_contact

    def set_i_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb2dict[word] = (self.id, self.prepositions)

    def no_vis_notice1(self, thing):
        assert isinstance(thing, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing.art_d()} ' + f' because there is no {thing.art_d()} here.')

    def no_vis_notice2(self, thing1, thing2):
        assert isinstance(thing1, str), 'This function requires a string input.'
        assert isinstance(thing2, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing1} ' + self.id[self.id.index('_') + 1:].replace('|', ' ') + ' the' + f' {thing2.get_name()}' + ' because there is no ' + thing2.get_name() + ' here.')

    def disambiguate_d_o(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        return potentials

    def disambiguate_i_o(self, d_o, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_i_o_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + d_o.get_name() + ' ' + after_(self.id.replace('|', ' ')) + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_i_o_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    return(f'#You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + d_o.get_name() + ' ' + after_(self.id.replace('|', ' ')) + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize_i_o(d_o, x))
        return self.infer_nouns(prioritized_thinglist)

    def prioritize_d_o(self, thing):
        return (thing, 0)

    def prioritize_i_o(self, thing1, thing2):
        return (thing2, 0)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        return new

    def execute(self, d_o, i_o):
        d_o = d_o.replace('_', ' ')
        if self in i_o.get_remaps_i():
            i_o = i_o.get_remaps_i()[self]
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            if i_o.i_o_check(self, d_o):
                self.body(d_o, i_o)
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self, d_o, i_o):
        pass

class Verb2Lit:

    def __init__(self, id, synonyms, prepositions):
        assert type(id) == str, 'The internal id of the verb must be a string.'
        assert type(synonyms) == list, 'The synonyms must be in a list.'
        assert type(prepositions) == tuple, 'The prepositions must be in a tuple.'
        for x in synonyms:
            assert type(x) == str, 'All synonyms must be strings.'
        for x in prepositions:
            assert type(x) == str, 'All prepositions must be strings.'
        self.id = id
        self.synonyms = synonyms
        self.prepositions = prepositions
        for x in synonyms:
            verb2litdict[x] = (self.id, self.prepositions)
        verb_id_dict[self.id] = self
        self.d_o_requires_sight = True
        self.d_o_requires_contact = True
        self.i_o_requires_sight = True
        self.i_o_requires_contact = True
        self.forbidden_states = []
        self.required_states = []

    def get_forbidden_states(self):
        return self.forbidden_states

    def get_required_states(self):
        return self.required_states

    def set_forbidden_states(self, l):
        assert type(l) == list, 'The forbidden states must be in a list.'
        for x in l:
            assert type(x) == str, 'The forbidden states must all be strings.'
        self.forbidden_states = l

    def set_required_states(self, l):
        assert type(l) == list, 'The required states must be in a list.'
        for x in l:
            assert type(x) == str, 'The required states must all be strings.'
        self.required_states = l

    def get_d_o_requires_sight(self):
        return self.d_o_requires_sight

    def set_d_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_sight = val

    def get_d_o_requires_contact(self):
        return self.d_o_requires_contact

    def set_d_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.d_o_requires_contact = val

    def get_i_o_requires_sight(self):
        return self.i_o_requires_sight

    def set_i_o_requires_sight(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_sight = val

    def get_i_o_requires_contact(self):
        return self.i_o_requires_contact

    def set_i_o_requires_contact(self, val):
        assert type(val) == bool, 'The value must be a boolean.'
        self.i_o_requires_contact = val

    def add_synonym(self, word):
        assert type(word) == str, 'All synonyms must be strings.'
        self.synonyms.append(word)
        verb2dict[word] = (self.id, self.prepositions)

    def no_vis_notice1(self, thing):
        assert isinstance(thing, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing.art_d()} ' + f' because there is no {thing.art_d()} here.')

    def no_vis_notice2(self, thing1, thing2):
        assert isinstance(thing1, str), 'This function requires a string input.'
        assert isinstance(thing2, Object), 'Only objects can have visibility checked.'
        pront('You cannot ' + self.id[:self.id.index('_')].replace('|', ' ') + f' {thing1} ' + self.id[self.id.index('_') + 1:].replace('|', ' ') + ' the' + f' {thing2.get_name()}' + ' because there is no ' + thing2.get_name() + ' here.')

    def disambiguate_d_o(self, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        i = ''
        for x in multinoundict:
            if potentials == stringify_tuple(multinoundict[x]):
                i = x
                break
        for x in noundict:
            if potentials == noundict[x]:
                i = x
                break
        wordlist = potentials.split('~')
        thinglist = []
        for x in wordlist:
            thinglist.append(noun_id_dict[x])
        new_thinglist = thinglist.copy() #don't edit a list that's being looped over
        for x in thinglist:
            if (self.get_d_o_requires_sight() and not x.is_visible()):
                new_thinglist.remove(x)
        if len(new_thinglist) == 0:
            return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + i + ' because there is no ' + i + ' here.')
        newest_thinglist = new_thinglist.copy()
        for x in new_thinglist:
            if (self.get_d_o_requires_contact() and not x.is_reachable()):
                newest_thinglist.remove(x)
        if len(newest_thinglist) == 0:
            if len(new_thinglist) == 1:
                thing = new_thinglist[0]
                if 'distant' in thing.get_properties():
                    return (f'#You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
                elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
                    return(f'#You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
                elif isinstance(thing.get_loc(), Container):
                    return (f'#You cannot reach {thing.art_d()} through a closed container.')
            else:
                return('#You cannot ' + before_(self.id.replace('|', ' ')) + ' the ' + i + ' because you cannot reach any ' + i + '.')
        prioritized_thinglist = [] #list with the priorities assigned
        for x in newest_thinglist:
            prioritized_thinglist.append(self.prioritize_d_o(x))
        return self.infer_nouns(prioritized_thinglist)

    def disambiguate_i_o(self, d_o, potentials):
        assert type(potentials) == str, 'Only strings can be disambiguated.'
        return potentials

    def prioritize_d_o(self, thing):
        return (thing, 0)

    def prioritize_i_o(self, thing):
        return (thing, 0)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        return new

    def execute(self, d_o, i_o):
        if self in d_o.get_remaps_d():
            d_o = d_o.get_remaps_d()[self]
        i_o = i_o.replace('_', ' ')
        if (player.get_state() in self.get_required_states() or len(self.get_required_states()) == 0) and player.get_state() not in self.get_forbidden_states():
            if d_o.d_o_check(self):
                self.body(d_o, i_o)
        else:
            pront(f'You cannot do that while {player.get_state()}.')

    def body(self, d_o, i_o):
        pass

class Timer:

    def __init__(self):
        self.active = False
        self.dur = 0
        self.start_turn = 0
        MasterState.event_list.append(self)

    def activate(self):
        if not self.active:
            self.active = True
            self.start_turn = MasterState.turn_count

    def deactivate(self):
        self.active = False

    def reactivate(self):
        self.active = True
        self.start_turn = MasterState.turn_count

    def get_activity(self):
        return self.active

    def set_dur(self, n):
        assert (type(n) == int) and (n >= 0), 'The duration must be a non-negative integer.'
        self.dur = n

    def get_dur(self):
        return self.dur

    def get_start_turn(self):
        return self.start_turn

    def engage(self):
        self.deactivate()

class Pulser(Timer):

    def engage(self):
        self.reactivate()
        self.start_turn += 1

class AestheticPulser(Pulser):

    def __init__(self):
        super().__init__()
        self.percent = 100
        self.messages = []

    def get_percent(self):
        return self.percent

    def set_percent(self, n):
        assert (type(n) == int) and (n >= 0) and (n <= 100), 'The percentage must be an integer or float, greater than or equal to zero and less than or equal to one hundred.'
        self.percent = n

    def get_messages(self):
        return self.messages

    def add_message(self, msg):
        assert type(msg) == str, 'The message must be a string.'
        self.messages.append(msg)

    def remove_message(self, msg):
        assert type(msg) == str, 'The message must be a string.'
        if msg in self.get_messages():
            self.messages.remove(msg)

    def set_messages(self, l):
        assert type(l) == list, 'The messages must be in the form of a list.'
        for x in l:
            assert type(x) == str, 'The messages must all be strings.'
        self.messages = l

    def get_room_list(self):
        return self.room_list

    def add_room(self, r):
        assert isinstance(r, Room), 'The room must be an actual room.'
        self.room_list.append(r)

    def remove_room(self, r):
        assert isinstance(r, Room), 'The room must be an actual room.'
        if room in self.get_room_list():
            self.room_list.remove(r)

    def set_rooms(self, l):
        assert type(l) == list, 'The rooms must be in the form of a list.'
        for x in l:
            assert type(x) == str, 'The rooms must all be actual rooms.'
        self.room_list = l

    def engage(self):
        super().engage()
        if (random.randint(0, 100) <= self.get_percent()) and player.get_loc() in self.get_room_list():
            pront(choose(self.get_messages()))

class GreetingPulser(Pulser):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def engage(self):
        super().engage()
        if self.get_owner().get_loc() == player.get_loc() and MasterState.turn_count - self.get_owner().get_greet_dur() >= self.get_owner().get_last_greet_turn() and player.get_loc() != player.get_prior_loc() and not self.get_owner().ownfollowPulser.get_activity():
            self.get_owner().greet_player()
            self.get_owner().set_last_greet_turn(MasterState.turn_count)
            if self.get_owner().ownwanderPulser.get_activity():
                self.get_owner().ownwanderPulser.reactivate()

    def get_owner(self):
        return self.owner

    def set_owner(self):
        raise Exception('Do not attempt to change the owner of an NPC greeting schedule. You will crash the program. Why would you ever attempt this?')

class WanderPulser(Pulser):

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def get_owner(self):
        return self.owner

    def set_owner(self):
        raise Exception('Do not attempt to change the owner of an NPC wander schedule. You will crash the program. Why would you ever attempt this?')

    def keytest(self, door):
        for x in door.get_keylist():
            if x.get_loc() == self.get_owner():
                return True
        return False

    def engage(self):
        super().engage()
        l = []
        oldloc = self.get_owner().get_loc()
        k = self.get_owner().get_loc().get_exits()
        for x in k:
            if isinstance(k[x][0], Room):
                if k[x][0] in self.get_owner().get_room_list():
                    l.append(x)
            elif isinstance(k[x][0], Door):
                if k[x][0].get_connection().get_loc() in self.get_owner().get_room_list():
                    l.append(x)
        d = choose(l)
        if isinstance(k[d][0], Room):
            if self.get_owner().get_loc() == player.get_loc():
                if d == 'u':
                    pront(f'{self.get_owner().art_d().capitalize()} ascends out of view.')
                elif d == 'd':
                    pront(f'{self.get_owner().art_d().capitalize()} descends out of view.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} walks out to the {directionsdict[d]}.')
            self.get_owner().warp_to(k[d][0])
            newloc = k[d][0]
            d2 = ''
            if self.get_owner().get_loc() == player.get_loc():
                for y in newloc.get_exits():
                    if newloc.get_exits()[y][0] == oldloc:
                        d2 = y
                if d2 != '':
                    if d2 == 'u':
                        pront(f'{self.get_owner().art_d().capitalize()} comes down from above.')
                    elif d2 == 'd':
                        pront(f'{self.get_owner().art_d().capitalize()} comes up from below.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} walks in from the {directionsdict[d2]}.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} walks into the room.')
        elif isinstance(k[d][0], KeyedDoor) and not k[d][0].is_open(): #if attempting to go through a closed keyed door
            if self.keytest(k[d][0]) or not k[d][0].is_locked():
                if self.get_owner().get_loc() == player.get_loc():
                    if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                        pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()}, goes through {obliquefy(k[d][0].pluralize("it"))}, and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()} and goes through {obliquefy(k[d][0].pluralize("it"))}.')
                self.get_owner().warp_to(k[d][0].get_connection().get_loc())
                if not (k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list()):
                    k[d][0].make_open(); k[d][0].unlock()
                if self.get_owner().get_loc() == player.get_loc():
                    if self.get_owner().get_loc() == player.get_loc():
                        if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                            pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                        else:
                            pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()}.')
        elif isinstance(k[d][0], LockedDoor) and not k[d][0].is_open(): #if attempting to go through a closed keyed door
            if self.get_owner().get_loc() == player.get_loc():
                if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                    pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()}, goes through {obliquefy(k[d][0].pluralize("it"))}, and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()} and goes through {obliquefy(k[d][0].pluralize("it"))}.')
            self.get_owner().warp_to(k[d][0].get_connection().get_loc())
            if not (k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list()):
                k[d][0].make_open(); k[d][0].unlock()
            if self.get_owner().get_loc() == player.get_loc():
                if self.get_owner().get_loc() == player.get_loc():
                    if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()}.')
        elif isinstance(k[d][0], Door) and not k[d][0].is_open(): #if attempting to go through a closed keyed door
            if self.get_owner().get_loc() == player.get_loc():
                if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                    pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()}, goes through {obliquefy(k[d][0].pluralize("it"))}, and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} opens {k[d][0].art_d()} and goes through {obliquefy(k[d][0].pluralize("it"))}.')
            self.get_owner().warp_to(k[d][0].get_connection().get_loc())
            if not (k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list()):
                k[d][0].make_open()
            if self.get_owner().get_loc() == player.get_loc():
                if self.get_owner().get_loc() == player.get_loc():
                    if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()}.')
        else:
            if self.get_owner().get_loc() == player.get_loc():
                if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                    pront(f'{self.get_owner().art_d().capitalize()} goes through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                else:
                    pront(f'{self.get_owner().art_d().capitalize()} goes through {k[d][0].art_d()}.')
            self.get_owner().warp_to(k[d][0].get_connection().get_loc())
            if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                k[d][0].make_closed()
                if isinstance(d, KeyedDoor) and self.keytest(d) or isinstance(d, LockedDoor):
                    k[d][0].make_locked()
            if self.get_owner().get_loc() == player.get_loc():
                if self.get_owner().get_loc() == player.get_loc():
                    if k[d][0].get_connection().get_loc() in self.get_owner().get_private_list() or k[d][0].get_loc() in self.get_owner().get_private_list():
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()} and closes {obliquefy(k[d][0].pluralize("it"))} behind {reflexify(self.get_owner().get_pronoun())}.')
                    else:
                        pront(f'{self.get_owner().art_d().capitalize()} comes in through {k[d][0].art_d()}.')
        self.get_owner().set_prior_loc(oldloc)
        if self.get_owner().get_loc() == player.get_loc() and MasterState.turn_count - self.get_owner().get_greet_dur() >= self.get_owner().get_last_greet_turn():
            self.get_owner().greet_player()
            self.get_owner().set_last_greet_turn(MasterState.turn_count)

class FollowPulser(Pulser):

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def get_owner(self):
        return self.owner

    def set_owner(self):
        raise Exception('Do not attempt to change the owner of an NPC follow schedule. You will crash the program. Why would you ever attempt this?')

    def engage(self):
        super().engage()
        if player.get_loc() != player.get_prior_loc():
            self.get_owner().set_prior_loc(self.get_owner().get_loc())
            self.get_owner().warp_to(player.get_loc())
            pront(self.get_owner().get_activity_desc())

def sequence(words, conj):
    assert type(words) == list, 'The words must be in a list.'
    for x in words:
        assert type(x) == str, 'All words must be strings.'
    assert type(conj) == str, 'The conjunction must be a string.'
    if len(words) == 1:
        return words[0]
    elif len(words) == 2:
        return words[0] + ' ' + conj + ' ' + words[1]
    else:
        temp = ''
        for x in range(len(words) - 1):
            temp += words[x]; temp += ', '
        temp += conj; temp += ' '; temp += words[-1]
        return temp

def beautify_sequence(words, conj):
    assert type(words) == list, 'The words must be in a list.'
    for x in words:
        assert type(x) == str, 'All words must be strings.'
    assert type(conj) == str, 'The conjunction must be a string.'
    if len(words) == 1:
        return 'the ' + beautify_noun(words[0])
    elif len(words) == 2:
        return 'the ' + beautify_noun(words[0]) + ' ' + conj + ' the ' + beautify_noun(words[1])
    else:
        temp = ''
        for x in range(len(words) - 1):
            temp += 'the '; temp += beautify_noun(words[x]); temp += ', '
        temp += conj; temp += ' the '; temp += beautify_noun(words[-1])
        return temp

def before_(text):
    return (text[:text.index('_')])

def after_(text):
    return (text[text.index('_') + 1:])

class Perception():
    def __init__(self, source):
        assert isinstance(source, Room) or isinstance(source, Object), 'The source of the perception must be a room or an object.'
        self.source = source
        self.desc = 'You perceive something.'
        self.invisible_desc = 'You perceive something.'
        self.activity = True
        self.is_smell = False
        self.is_sound = False

    def make_sound(self):
        self.source.set_sound_description(self)
        self.is_smell = False
        self.is_sound = True

    def make_smell(self):
        self.source.set_smell_description(self)
        self.is_smell = True
        self.is_sound = False

    def is_sound(self):
        return self.is_sound

    def is_smell(self):
        return self.is_smell

    def set_description(self, desc):
        assert isinstance(desc, str), 'The description must be a string.'
        self.desc = desc

    def set_invisible_description(self, desc):
        assert isinstance(desc, str), 'The invisible description must be a string.'
        self.invisible_desc = desc

    def get_description(self):
        return self.desc

    def get_invisible_description(self):
        return self.invisible_desc

    def get_source(self):
        return self.source

    def get_activity(self):
        return self.activity

class PerceptionLink():
    def __init__(self, input, output):
        assert isinstance(input, Object), 'The perception input must be an object.'
        assert isinstance(output, Object), 'The perception output must be an object.'
        self.input = input
        self.output = output
        self.transparent_sound = False
        self.transparent_smell = False
        self.activity = True
        self.inactive_sound_description = 'You hear nothing.'
        self.inactive_smell_description = 'You smell nothing.'

    def get_input(self):
        return self.input

    def get_output(self):
        return self.output

    def connect_sound(self):
        self.output.set_sound_description(self)
        self.transparent_sound = True

    def connect_smell(self):
        self.output.set_smell_description(self)
        self.transparent_sound = True

    def get_transparent_sound(self):
        return self.transparent_sound

    def get_transparent_smell(self):
        return self.transparent_smell

    def activate(self):
        self.activity = True

    def deactivate(self):
        self.activity = False

    def get_activity(self):
        return self.activity

    def get_inactive_sound_description(self):
        return self.inactive_sound_description

    def get_inactive_smell_description(self):
        return self.inactive_smell_description

    def set_inactive_sound_description(self, desc):
        assert isinstance(desc, str), 'The description must be a string.'
        self.inactive_sound_description = desc

    def set_inactive_smell_description(self, desc):
        assert isinstance(desc, str), 'The description must be a string.'
        self.inactive_smell_description = desc

class MasterState():
    turn_count = 0
    win_states = {
    0 : 'You push the button and the station computer begins sending a distress call to all nearby vessels. Within moments the repair ship FCS Renzo Piano has responded to your call, and informs you that they will arrive at your position within seventeen hours. With the situation under control for the moment and help on the way, you decide to crawl into your bunk and take a nap. Today has been a long day.'
    }
    lose_states = {
    0 : 'Exposure to a vacuum environment without a spacesuit typically produces fatal results. Your situation is no exception: you die of hypoxia.',
    1 : 'Your spacesuit offers protection against the vacuum of space, but you still need an air tank to breathe from. You have suffocated.',
    2 : 'You die of suffocation after exhausting your air supply.'
    }

    event_list = []

def win(n):
    assert n in MasterState.win_states
    print()
    pront(MasterState.win_states[n])
    print()
    raise SystemExit(0)

def lose(n):
    assert n in MasterState.lose_states
    print()
    pront(MasterState.lose_states[n])
    print()
    raise SystemExit(0)

def inc_turn():
    run_events()
    player.set_prior_loc(player.get_loc())
    MasterState.turn_count += 1

def run_events():
    for x in MasterState.event_list:
        if x.get_activity() and x.get_dur() + x.get_start_turn() == MasterState.turn_count:
            x.engage()

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

def pront(text): #printing, but with wrapped text (will not work for blank lines, use print() instead, fixed so that it will interpret \n correctly)
    print(textwrap.fill(text, width = 80, replace_whitespace = False))

def choose(somelist):
    return somelist[random.randint(0,len(somelist) - 1)]

def no_reach_notice(thing):
    assert isinstance(thing, Object), 'Only objects can have reachability checked.'
    if 'distant' in thing.get_properties():
        pront(f'You cannot reach {thing.art_d()} because {thing.pluralize("it is")} too far away.')
    elif hasattr(player, 'state_position') and not (thing.is_within(player.get_state_position()) or thing.is_within(player)):
        pront(f'You cannot reach {thing.art_d()} from {player.get_state_position().art_d()}.')
    elif isinstance(thing.get_loc(), Container):
        pront(f'You cannot reach {thing.art_d()} through a closed container.')

define_again_verbs(['g','again', 'do again', 'do it again', 'do it over', 'do over'])

def start_message():
    print()
    pront('Welcome to The Comm after the Storm, the first game written in the complete Ekphrastic Engine. First-time players should type "help" for more info.')
    print()
    c = True
    while c:
        pront('(Press enter to continue)')
        print()
        m = input('> ').lower().strip()
        if m in ['help', 'help me']:
            help.body()
        else:
            c = False
        print()
    pront('A two-month post manning the deep-space communications station for sector epsilon-916 was supposed to be a routine (if rather lonely) job. Instead, you found yourself sheltering in the station airlock as a freak meteor shower bombarded the hull. A cacophony of alarms signalled the loss of internal pressure, only to be silenced moments later by the loss of main power. Now, with the meteor bombardment over, it is time to assess the damage.')
    print()
    player.know_objects_in_loc(player.get_loc())
    player.get_loc().describe()
    print()

#rooms

class StationRoom(InsideRoom):

    def __init__(self):
        super().__init__()
        self.atmosphere = False

    def get_atmosphere(self):
        return self.atmosphere

    def set_atmosphere(self, n):
        assert type(n) == bool, 'The atmosphere value must be a boolean.'
        self.atmosphere = n

class SpaceRoom(Room):

    def __init__(self):
        super().__init__()
        self.atmosphere = False

    def get_atmosphere(self):
        return self.atmosphere

    def describe(self):
        if self.is_illuminated():
            pront(self.desc)
            for x in self.get_contents():
                if x != player and not isinstance(x, NPC) and 'hidden' not in x.get_properties():
                    if 'initialize' in x.get_properties():
                        pront(x.init_desc)
                    elif ('unlisted' in x.get_properties()) and isinstance(x, Surface) and len(x.get_contents()) > 0:
                        pront(f'{x.art_d().capitalize()} {x.pluralize("bears")}:')
                        x.list_contents(1)
                    elif ('unlisted' in x.get_properties()) and isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()):
                        pront(f'{x.art_d().capitalize()} {x.pluralize("contains")}:')
                        x.list_contents(1)
            for y in self.get_contents():
                w = ''
                if isinstance(y, RopeTrail) and y.is_visible():
                    k = y.get_parent_rope()
                    if k.get_tied_objects()[0].is_visible():
                        if 'plug' in k.get_properties():
                            w += f' (plugged into '
                        else:
                            w += f' (tied to '
                        if len(k.get_tied_objects()) == 1:
                            w += f'{k.get_tied_objects()[0].art_d()})'
                        elif len(k.get_tied_objects()) == 2:
                            w += f'{k.get_tied_objects()[0].art_d()} and {k.get_tied_objects()[1].art_d()})'
                        pront(f'There {k.pluralize("is")} {k.art_i()}{w} here.')
                    elif len(k.get_tied_objects()) > 1 and k.get_tied_objects()[1].is_visible():
                        if 'plug' in k.get_properties():
                            w += f' (plugged into '
                        else:
                            w += f' (tied to '
                        w += f'{k.get_tied_objects()[1].art_d()})'
                        pront(f'There {k.pluralize("is")} {k.art_i()}{w} here.')
                    else:
                        pront(f'There {k.pluralize("is")} {k.art_i()} running across the hull here.')
                if ('unlisted' not in y.get_properties()) and ('initialize' not in y.get_properties() and 'hidden' not in y.get_properties()):
                    if 'plug' in y.get_properties() and isinstance(y, Rope):
                        w += f' (plugged into '
                    elif isinstance(y, Rope):
                        w += f' (tied to '
                    if isinstance(y, Rope) and len(y.get_tied_objects()) == 1:
                        w += f'{y.get_tied_objects()[0].art_d()})'
                    if isinstance(y, Rope) and len(y.get_tied_objects()) == 2:
                        w += f'{y.get_tied_objects()[0].art_d()} and {y.get_tied_objects()[1].art_d()})'
                    if hasattr(y, 'parent_attachment'):
                        if 'plug' in y.get_properties():
                            w += f' (plugged into {y.get_parent_attachment().art_d()})'
                        else:
                            w += f' (attached to {y.get_parent_attachment().art_d()})'
                    if 'lamp' in y.get_properties() and y.get_brightness() == 2:
                        w += ' (lit)'
                    pront(f'There {y.pluralize("is")} {y.art_i()}{w} floating nearby here.')
                    if isinstance(y, Surface) and len(y.get_contents()) > 0:
                        pront(f'{y.art_d().capitalize()} {y.pluralize("bears")}:')
                        y.list_contents(1)
                    elif isinstance(y, Container) and len(y.get_contents()) > 0 and (y.is_open() or y.is_transparent()):
                        pront(f'{y.art_d().capitalize()} {y.pluralize("contains")}:')
                        y.list_contents(1)
            for z in self.get_contents():
                if isinstance(z, NPC) and 'hidden' not in z.get_properties():
                    pront(z.get_activity_desc())
        else:
            pront(self.dark_desc)
            for x in self.get_contents():
                if x.get_brightness() == 1:
                    if x != player and not isinstance(x, NPC) and 'hidden' not in x.get_properties():
                        if 'initialize' in x.get_properties():
                            pront(x.init_desc)
                        elif ('unlisted' in x.get_properties()) and isinstance(x, Surface) and len(x.get_contents()) > 0:
                            pront(f'{x.art_d().capitalize()} {x.pluralize("bears")}:')
                            x.list_contents(1)
                        elif ('unlisted' in x.get_properties()) and isinstance(x, Container) and len(x.get_contents()) > 0 and (x.is_open() or x.is_transparent()):
                            pront(f'{x.art_d().capitalize()} {x.pluralize("contains")}:')
                            x.list_contents(1)
            for y in self.get_contents():
                if y.get_brightness() == 1:
                    if ('unlisted' not in y.get_properties()) and ('initialize' not in y.get_properties() and 'hidden' not in y.get_properties()):
                        pront(f'There {y.pluralize("is")} {y.art_i()} floating nearby here.')
                        if isinstance(y, Surface) and len(y.get_contents()) > 0:
                            pront(f'{y.art_d().capitalize()} {y.pluralize("bears")}:')
                            y.list_contents(1)
                        elif isinstance(y, Container) and len(y.get_contents()) > 0 and (y.is_open() or y.is_transparent()):
                            pront(f'{y.art_d().capitalize()} {y.pluralize("contains")}:')
                            y.list_contents(1)
            for z in self.get_contents():
                if y.get_brightness() == 1:
                    if isinstance(z, NPC) and 'hidden' not in z.get_properties():
                        pront(z.get_activity_desc())
        if self.is_noisy():
            self.describe_sound(True)
        if self.is_smelly():
            self.describe_smell(True)

class AirlockExterior(SpaceRoom):
    def travelcheck(self, dir):
        if dir == 'u' and not self.is_illuminated():
            pront('There are handholds that would let you climb the exterior of the hull, but they are not visible in the dark.')
            return False
        return True

class DebrisRoom(StationRoom):
    def travelcheck(self, dir):
        if dir == 'n' and debris.get_loc() is self:
            pront('The collapsed beam blocks your passage.')
            return False
        return True

airlock = StationRoom()
airlock_exterior = AirlockExterior()
engineering = StationRoom()
corridor1 = StationRoom()
corridor2 = StationRoom()
corridor3 = StationRoom()
corridor4 = DebrisRoom()
solar_fin_control = StationRoom()
outer_hull_1 = SpaceRoom()
outer_hull_2 = SpaceRoom()
outer_hull_3 = SpaceRoom()
cargo_hold = StationRoom()
quarters = StationRoom()
bridge = StationRoom()

airlock.set_atmosphere(True)
airlock.set_description('This sturdily constructed chamber is designed to remain pressurized even under extreme stress, so it was the logical place to seek refuge during the meteor storm. The airlock controls are mounted to the wall in front of you. On the opposite wall is an equipment rack. The interior airlock door is to the west, and the exterior airlock door is to the east.')

corridor1.set_description('This corridor runs the length of the station. Most of the station lies to the north; to your south the corridor ends where it meets the engine room. To the east is the door to the airlock chamber.')
corridor1.add_exit('s', engineering, 'You emerge from the corridor and find yourself in the station\'s engine room.')
corridor1.add_exit('n', corridor2, 'You walk north along the corridor.')

airlock_exterior.make_dark()
airlock_exterior.set_description('You are perched at a small platform on the dark side of the station. Normally this would serve as the gangway to any ship docked at the station, but right now your station is the only vessel around for light-years. The platform bears a power socket that is used to transfer power to docked ships. The airlock door to the interior of the station is to the west, and a set of handholds on the station\'s outer hull lead upwards.')
airlock_exterior.set_dark_desc('This side of the station faces away from the local star system\'s sun. Consequently, it is pitch-black here. To the west you are only barely able to make out the airlock door leading back into the station.')
airlock_exterior.add_exit('u', outer_hull_1, 'You climb the handholds that lead up the station\'s outer hull.')

engineering.add_exit('n', corridor1, 'You walk into the main corridor.')
engineering.set_description('The engine room sits at the back of the station, and houses essential systems such as life support and power distribution. At the center of the room you find the primary control panel for these systems; mounted on the wall are a power cell charger and a high-pressure air pump.')

corridor2.set_description('This north-south corridor runs the length of the station. A branch to the east leads to the solar fin control room. Evidently this section was hit hard by the meteors: a fist-sized hole straight through the titanium-ceramic plating seems to have let the station atmosphere out into the void.')
corridor2.add_exit('s', corridor1, 'You walk south along the corridor.')
corridor2.add_exit('n', corridor3, 'You walk north along the corridor.')
corridor2.add_exit('e', solar_fin_control, 'You walk east through the branch corridor.')

corridor3.set_description('This north-south corridor runs the length of the station. A branch corridor to the west leads to the cargo hold.')
corridor3.add_exit('s', corridor2, 'You walk south along the corridor.')
corridor3.add_exit('n', corridor4, 'You walk north along the corridor.')
corridor3.add_exit('w', cargo_hold, 'You take the branch west to the cargo hold.')

corridor4.set_description('The main corridor terminates here, at the entrance to the living quarters. The way north is obstructed by debris, namely a collapsed support beam blocking the entrance. The corridor stretches away to the south.')
corridor4.add_exit('s', corridor3, 'You walk south along the corridor.')
corridor4.add_exit('n', quarters, 'You walk north along the corridor.')

cargo_hold.set_description('This small cargo hold is where the station\'s supplies are stored. A crate sitting at the center of the room beckons your attention; there is also a winch bolted to the floor next to it. A power socket sits on the wall next to the start of the branch corridor, which leads east to the main corridor.')
cargo_hold.add_exit('e', corridor3, 'You pass through the branch corridor and find yourself back in the main one.')

solar_fin_control.set_description('The controls that operate the station\'s solar fin are housed in this room. A button labeled "extend fin" is mounted next to a status display. Below the controls there is a power socket. The way back to the main corridor is to the west.')
solar_fin_control.add_exit('w', corridor2, 'You return to the main corridor.')

quarters.set_description('These living quarters are where you spend most of your downtime on the station. An alcove on one wall houses your bed, which sits atop a pullout drawer. On the opposite wall there is a video monitor and a power socket. The main station corridor leads out of the room to the south. To the north, a security door bars the way to the bridge.')
quarters.add_exit('s', corridor4, 'You walk back into the main corridor.')

outer_hull_1.make_dark()
outer_hull_1.set_description('You cling to a set of handholds affixed to the outer hull of the station. They continue both upwards, towards the solar fin and the antenna, and downwards, to the airlock.')
outer_hull_1.set_dark_desc('This section of the hull is only marginally brighter than the section immediately below you. You can barely see handholds leading upwards and downwards, but that is it.')
outer_hull_1.add_exit('u', outer_hull_2, 'You climb up and emerge onto the lit half of the station.')
outer_hull_1.add_exit('d', airlock_exterior, 'You climb down towards the airlock exterior.')

outer_hull_2.set_description('This part of the station is well lit because it faces the local sun. As such, it was the logical place to put the station\'s solar fin. Unfortunately, a meteor appears to have struck here: a chunk of rock stuck in the extension mechanism is preventing the solar fin from extending. Handholds here lead up and down.')
outer_hull_2.add_exit('u', outer_hull_3, 'You climb upwards to the very top of the station.')
outer_hull_2.add_exit('d', outer_hull_1, 'You descend back into darkness.')

outer_hull_3.set_description('At the pinnacle of the station is its reason for existence: the antenna here is responsible for relaying communications across three entire sectors (and part of a fourth). A panel at the base of the antenna provides access to the electronics serving it. The only way out is to follow the handholds back down.')
outer_hull_3.add_exit('d', outer_hull_2, 'You climb back towards the solar fin.')

bridge.set_description('All the communications sent through the station are monitored from the bridge. At the center of the room is the command chair, which faces a console full of myriad buttons. Out of all these, the one that intrests you most right now is the large red one labeled "distress." If you can get a message out, a repair ship will respond to the station and help restore it to working order. The only exit from the bridge is the security door to the south.')

#player stuff
player.warp_to(airlock)
player.set_description('At the moment, you happen to be yourself. It would be concerning if this were not so.')
player.add_property('unlisted')
player.add_property('custom_immobile')
player.set_custom_immobile_message('To attempt such a feat would be incredibly foolish.')
player.set_definite_article('')
player.set_indefinite_article('')
player.make_known()

hands = Object('hands', 'hands', ['hands', 'hand'])
hands.set_description('They are your own two hands.')
hands.set_bulk(0)
hands.warp_to(player)
hands.add_property('player_anatomy')
hands.set_definite_article('your')
hands.set_indefinite_article('your')
hands.make_plural()
#end of player stuff

bridge_console = Object('console', 'console', ['console', 'command console', 'communications console'])
bridge_console.add_property('immobile')
bridge_console.add_property('unlisted')
bridge_console.set_description('There are many buttons on this console, but the one that matters to you now is red and labeled "distress."')
bridge_console.warp_to(bridge)

red_button = Object('red button', 'red_button', ['red button', 'button', 'distress button', 'red distress button', 'red'])
red_button.make_component_of(bridge_console)

command_chair = Chair('command chair', 'command_chair', ['command chair', 'chair'])
command_chair.warp_to(bridge)
command_chair.add_property('unlisted')
command_chair.set_description('While seated in this chair, more than three sectors worth of communications data are available at your fingertips. At least, they would be if the station were operational.')

rack = Surface('equipment rack', 'equipment_rack', ['equipment rack', 'rack'])
rack.warp_to(airlock)
rack.set_description('A sturdy fixture designed to hold useful equipment for excursions outside the station.')
rack.add_property('anchored')
rack.add_property('unlisted')

class Spacesuit(Object):
    def i_o_check(self, v, d_o):
        if v is attach:
            if d_o in [drill, lamp, welder]:
                if drill in spacesuit.get_child_attachments() and d_o is not drill:
                    pront(f'You cannot attach {d_o.art_d()} to the spacesuit while the drill is attached to it.')
                    return False
                elif lamp in spacesuit.get_child_attachments() and d_o is not lamp:
                    pront(f'You cannot attach {d_o.art_d()} to the spacesuit while the lamp is attached to it.')
                    return False
                elif welder in spacesuit.get_child_attachments() and d_o is not welder:
                    pront(f'You cannot attach {d_o.art_d()} to the spacesuit while the welder is attached to it.')
                    return False
                elif d_o is lamp and lamp not in spacesuit.get_child_attachments() and power_cell in spacesuit.get_child_attachments() and power_cell.get_charge() > 0:
                    pront(f'As soon as you attach the lamp to the suit it blinks on.')
                    d_o.attach_to(spacesuit)
                    inc_turn()
                    return False
            elif d_o is power_cell and power_cell not in spacesuit.get_child_attachments() and power_cell.get_charge() > 0 and lamp in spacesuit.get_child_attachments():
                pront(f'As soon as you attach the power cell to the suit the lamp blinks on.')
                d_o.attach_to(spacesuit)
                inc_turn()
                return False
        return True

spacesuit = Spacesuit('spacesuit', 'spacesuit', ['spacesuit', 'space suit', 'suit', 'my spacesuit', 'my space suit', 'my suit', 'your spacesuit', 'your space suit', 'your suit'])
spacesuit.warp_to(rack)
spacesuit.add_property('clothing')
spacesuit.set_indefinite_article('your')
spacesuit.set_definite_article('your')
spacesuit.set_description('This is your personal spacesuit: it is custom-sized to fit you and bears the circle-and-crescent insignia of a communications specialist. Two ports on the back are designed to fit an air tank and a power cell, while a smaller one on the wrist can accomodate and power auxiliary equipment.')

class Tank(Object):

    def set_air(self, n):
        assert type(n) == int and n >= 0, 'The air level must be a non-negative integer.'
        self.air = n

    def get_air(self):
        return self.air

    def describe(self):
        super().describe()
        pront(f'The gauge reads "{self.get_air()}/120 units."')

air_tank = Tank('air tank', 'air_tank', ['air tank', 'tank', 'oxygen tank', 'air cylinder', 'oxygen cylinder', 'cylinder', 'green tank', 'green cylinder'])
air_tank.warp_to(rack)
air_tank.set_description('The dark green coating sintered onto the tank indicates it is designed to contain breathable air. A gauge on the tank indicates the current air pressure.')
air_tank.add_allowed_parent_attachment(spacesuit)
spacesuit.add_allowed_child_attachment(air_tank)
air_tank.set_air(120)

class Cell(Object):

    def set_charge(self, n):
        assert type(n) == int and n >= 0, 'The charge level must be a non-negative integer.'
        self.charge = n

    def get_charge(self):
        return self.charge

    def describe(self):
        super().describe()
        pront(f'The meter reads "{self.get_charge()}/36 units."')

power_cell = Cell('power cell', 'power_cell', ['power cell', 'cell', 'rechargeable cell', 'rechargeable power cell', 'cylinder', 'silver cylinder', 'silver cell', 'silver power cell'])
power_cell.set_charge(36)
power_cell.warp_to(rack)
power_cell.set_description('This silver cylinder is a convenient portable power source. A meter on the side monitors the current level of charge; the cell can be recharged once depleted.')
power_cell.add_allowed_parent_attachment(spacesuit)
spacesuit.add_allowed_child_attachment(power_cell)
power_cell.set_bulk(5)

class Gauge(Object):

    def describe(self):
        pront(f'It reads "{self.get_parent_object().get_air()}/120 units."')

gauge = Gauge('gauge', 'gauge', ['gauge'])
gauge.make_component_of(air_tank)

class Meter(Object):

    def describe(self):
        pront(f'It reads "{self.get_parent_object().get_charge()}/36 units."')

meter = Meter('meter', 'meter', ['meter'])
meter.make_component_of(power_cell)

class SuitTool(Object):
    def d_o_check(self, v):
        if v == wear:
            if spacesuit.is_visible():
                attach.body(self, spacesuit)
            else:
                pront(f'{self.art_d().capitalize()} is designed to be worn attached to a spacesuit, but there does not seem to be a spaceuit nearby.')
            inc_turn()
            return False
        return True

drill = SuitTool('drill', 'drill', ['drill', 'wrist mounted drill', 'wrist-mounted drill'])
drill.warp_to(rack)
drill.set_description('A wrist-mounted drill designed to run on an exterior power source. The drill head can cut through all but the sturdiest materials.')
drill.add_allowed_parent_attachment(spacesuit)
spacesuit.add_allowed_child_attachment(drill)

handholds1 = Ladder('handholds', 'handholds#1', ['handholds', 'handhold', 'ladder', 'rungs', 'rung'])
handholds1.warp_to(airlock_exterior)
handholds1.set_description('These rungs are affixed to the exterior of the station, and are all that prevent you from drifting off to oblivion.')
handholds1.set_valid_up(True)
handholds1.set_up_destination(outer_hull_1)
handholds1.set_move_up_message('You climb the handholds that lead up the station\'s outer hull.')
handholds1.make_plural()

handholds2 = Ladder('handholds', 'handholds#2', ['handholds', 'handhold', 'ladder', 'rungs', 'rung'])
handholds2.warp_to(outer_hull_1)
handholds2.set_description('These rungs are affixed to the exterior of the station, and are all that prevent you from drifting off to oblivion.')
handholds2.set_valid_up(True)
handholds2.set_valid_down(True)
handholds2.set_up_destination(outer_hull_2)
handholds2.set_down_destination(airlock_exterior)
handholds2.set_move_up_message('You climb up and emerge onto the lit half of the station.')
handholds2.set_move_down_message('You climb down towards the airlock exterior.')
handholds2.make_plural()
handholds2.set_brightness(1)

handholds3 = Ladder('handholds', 'handholds#3', ['handholds', 'handhold', 'ladder', 'rungs', 'rung'])
handholds3.warp_to(outer_hull_2)
handholds3.set_description('These rungs are affixed to the exterior of the station, and are all that prevent you from drifting off to oblivion.')
handholds3.set_valid_up(True)
handholds3.set_valid_down(True)
handholds3.set_up_destination(outer_hull_3)
handholds3.set_down_destination(outer_hull_1)
handholds3.set_move_up_message('You climb upwards to the very top of the station.')
handholds3.set_move_down_message('You descend back down into darkness.')
handholds3.make_plural()

handholds4 = Ladder('handholds', 'handholds#4', ['handholds', 'handhold', 'ladder', 'rungs', 'rung'])
handholds4.warp_to(outer_hull_3)
handholds4.set_description('These rungs are affixed to the exterior of the station, and are all that prevent you from drifting off to oblivion.')
handholds4.set_valid_down(True)
handholds4.set_down_destination(outer_hull_2)
handholds4.set_move_down_message('You climb back towards the solar fin.')
handholds4.make_plural()

pump = Object('air pump', 'air_pump', ['air pump', 'pump', 'high pressure pump', 'high pressure air pump', 'high-pressure pump', 'high-pressure air pump'])
pump.warp_to(engineering)
pump.set_description('A high-pressure air pump designed to refill air tanks. There is a valve where an air tank can be attached.')
pump.add_property('unlisted')
pump.add_property('anchored')
pump.add_allowed_child_attachment(air_tank)
air_tank.add_allowed_parent_attachment(pump)

charger = Object('power cell charger', 'power_cell_charger', ['power cell charger', 'charger', 'cell charger'])
charger.warp_to(engineering)
charger.set_description('A device with a socket where a power cell can be attached and recharged.')
charger.add_property('unlisted')
charger.add_property('anchored')
charger.add_allowed_child_attachment(power_cell)
power_cell.add_allowed_parent_attachment(charger)

class Engine_control_panel(Object):
    def describe(self):
        super().describe()
        pront('The display indicates the following:')
        pront('Emergency lighting:  active')
        if not yellow_button.pressed and breach.get_loc() is not offstage:
            pront('Life support:        offline')
        else:
            pront('Life support:        online')
        if not solar_fin.extended:
            pront('Main solar power:    offline')
        else:
            pront('Main solar power:    online')
        if not yellow_button.pressed:
            pront('Emergency power:     available')
        else:
            pront('Emergency power:     activated')
        if antenna_axle.broken and not antenna_socket.is_powered():
            pront('Communications:      offline')
        else:
            pront('Communications:      online')
        if breach.get_loc() is not offstage:
            pront('Hull integrity:      breach in corridor near solar fin control')
        else:
            pront('Hull integrity:      intact')

engine_control_panel = Engine_control_panel('control panel', 'control_panel#engine', ['control panel', 'control', 'controls', 'panel', 'display', 'primary control panel', 'primary control', 'primary panel'])
engine_control_panel.add_property('unlisted')
engine_control_panel.add_property('anchored')
engine_control_panel.warp_to(engineering)
engine_control_panel.set_description('This control panel monitors the vital functions of the station. Most of the panel is taken up by a large display, but next to it there are a yellow button labeled "emergency power" and a green button labeled "life support reset."')

airlock_control_fixture = Object('control panel', 'control_panel#airlockfixture', ['control panel', 'panel', 'controls', 'control', 'airlock controls', 'airlock control'])
airlock_control_fixture.add_property('unlisted')
airlock_control_fixture.add_property('anchored')
airlock_control_fixture.warp_to(airlock)
airlock_control_fixture.set_description('The left button operates the interior door, the right button operates the exterior door, the lever in the middle depressurizes and repressurizes the airlock chamber, and a display above them all monitors the pressure both within and without. Beneath the controls is written the following message: "WARNING! DO NOT DEPRESSURIZE AIRLOCK WITHOUT WEARING SPACESUIT AND ATTACHED AIR SUPPLY!"')

class Display(Object):
    def describe(self):
        if airlock.get_atmosphere():
            pront('Airlock:   pressurized')
        else:
            pront('Airlock:   depressurized')
        if corridor1.get_atmosphere():
            pront('Interior:  pressurized')
        else:
            pront('Interior:  depressurized')
        if airlock_exterior.get_atmosphere():
            pront('Exterior:  pressurized')
        else:
            pront('Exterior:  depressurized')

display = Display('display', 'display', ['display', 'pressure display'])
display.warp_to(airlock)
display.add_property('unlisted')
display.add_property('anchored')
display.make_component_of(airlock_control_fixture)

lever = Object('lever', 'lever', ['lever', 'red lever', 'middle lever'])
lever.warp_to(airlock)
lever.add_property('unlisted')
lever.add_property('anchored')
lever.set_description('This red lever controls the atmosphere inside the airlock chamber. Pull it to switch pressurization on or off, but beware that depressurizing the airlock without wearing a spacesuit and air supply will have fatal consequences.')
lever.make_component_of(airlock_control_fixture)

left_button = Object('left button', 'left_button', ['left button', 'button', 'left'])
left_button.warp_to(airlock)
left_button.add_property('unlisted')
left_button.add_property('anchored')
left_button.set_description('This button will open and close the interior airlock door.')
left_button.make_component_of(airlock_control_fixture)

right_button = Object('right button', 'right_button', ['right button', 'button', 'right'])
right_button.warp_to(airlock)
right_button.add_property('unlisted')
right_button.add_property('anchored')
right_button.set_description('This button will open and close the exterior airlock door.')
right_button.make_component_of(airlock_control_fixture)

interior_airlock_door_1 = Door('interior airlock door', 'interior_airlock_door#1', ['interior airlock door', 'airlock door', 'door', 'interior door'])
interior_airlock_door_1.warp_to(airlock)
interior_airlock_door_1.set_description('A hefty titanium-ceramic door.')
interior_airlock_door_1.remove_property('openable')
interior_airlock_door_1.set_move_message('You step through the airlock door, into the station\'s main corridor.')
interior_airlock_door_1.add_property('enterable')
airlock.add_door('w', interior_airlock_door_1)

interior_airlock_door_2 = Door('interior airlock door', 'interior_airlock_door#2', ['interior airlock door', 'airlock door', 'door', 'interior door'])
interior_airlock_door_2.warp_to(corridor1)
interior_airlock_door_2.set_description('A hefty titanium-ceramic door.')
interior_airlock_door_2.remove_property('openable')
interior_airlock_door_2.set_move_message('You step through the airlock door, into the airlock chamber.')
interior_airlock_door_2.add_property('enterable')
corridor1.add_door('e', interior_airlock_door_2)
interior_airlock_door_2.set_connection(interior_airlock_door_1)

exterior_airlock_door_1 = Door('exterior airlock door', 'exterior_airlock_door#1', ['exterior airlock door', 'airlock door', 'door', 'exterior door'])
exterior_airlock_door_1.warp_to(airlock)
exterior_airlock_door_1.set_description('A hefty titanium-ceramic door.')
exterior_airlock_door_1.remove_property('openable')
exterior_airlock_door_1.set_move_message('You step through the airlock door and out of the space station.')
exterior_airlock_door_1.add_property('exitable')
airlock.add_door('e', exterior_airlock_door_1)

exterior_airlock_door_2 = Door('exterior airlock door', 'exterior_airlock_door#2', ['exterior airlock door', 'airlock door', 'door', 'exterior door'])
exterior_airlock_door_2.warp_to(airlock_exterior)
exterior_airlock_door_2.set_description('A hefty titanium-ceramic door.')
exterior_airlock_door_2.remove_property('openable')
exterior_airlock_door_2.set_move_message('You climb through the airlock door, back into the airlock chamber.')
exterior_airlock_door_2.add_property('enterable')
airlock_exterior.add_door('w', exterior_airlock_door_2)
exterior_airlock_door_2.set_connection(exterior_airlock_door_1)
exterior_airlock_door_2.set_brightness(1)

security_door_1 = Door('security door', 'security_door#1', ['security door', 'door'])
security_door_1.warp_to(quarters)
security_door_1.set_description('This titanium-ceramic, magnetically sealed door stands between you and the bridge. There is a small slot in the center of the door.')
security_door_1.remove_property('openable')
security_door_1.set_move_message('You step out onto the bridge.')
security_door_1.add_property('enterable')
quarters.add_door('n', security_door_1)

security_door_2 = Door('security door', 'security_door#2', ['security door', 'door'])
security_door_2.warp_to(bridge)
security_door_2.set_description('This titanium-ceramic, magnetically sealed door separates the bridge from the rest of the station.')
security_door_2.remove_property('openable')
security_door_2.set_move_message('You step back into the living quarters.')
security_door_2.add_property('exitable')
bridge.add_door('s', security_door_2)
security_door_2.set_connection(security_door_1)

class Slot(Container):
    def i_o_check(self, v, d_o):
        if v in [put, slide] and d_o is id_card:
            d_o.warp_to(slot)
            if security_door_1.is_open():
                security_door_1.make_closed()
                security_door_1.set_description('This titanium-ceramic, magnetically sealed door stands between you and the bridge. There is a small slot in the center of the door.')
                quarters.set_description('These living quarters are where you spend most of your downtime on the station. An alcove on one wall houses your bed, which sits atop a pullout drawer. On the opposite wall there is a video monitor and a power socket. The main station corridor leads out of the room to the south. To the north, a security door bars the way to the bridge.')
                pront('You put your identification card into the slot and the door shuts before you.')
            elif bridge_socket.is_powered():
                security_door_1.make_open()
                security_door_1.set_description('The security door is now open. The slot with your identification card in it is visible to one side.')
                quarters.set_description('These living quarters are where you spend most of your downtime on the station. An alcove on one wall houses your bed, which sits atop a pullout drawer. On the opposite wall there is a video monitor and a power socket. The main station corridor leads out of the room to the south. To the north, an open security door leads to the bridge.')
                pront('The security door slides open as soon as you insert your identification card.')
            else:
                pront('The security door remains obstinately closed. The power supply to the card reader must be interrupted.')
            inc_turn()
            return False
        return True

slot = Slot('slot', 'slot', ['slot', 'small slot', 'reader', 'card reader', 'thin slot'])
slot.make_component_of(security_door_1)
slot.set_description('A thin slot, not quite as wide as your hand.')


yellow_button = Object('yellow button', 'yellow_button', ['yellow button', 'button', 'power button', 'yellow'])
yellow_button.make_component_of(engine_control_panel)
yellow_button.set_description('The yellow button is labeled "emergency power."')
yellow_button.pressed = False

green_button = Object('green button', 'green_button', ['green button', 'button', 'life support button', 'reset button', 'life support reset button', 'green'])
green_button.make_component_of(engine_control_panel)
green_button.set_description('The green button is labeled "life support reset."')

fin_button = Object('button', 'button#fin', ['button', 'fin button', 'extend button', 'extension button', 'extend fin button', 'fin extension button', 'control', 'controls'])
fin_button.add_property('anchored')
fin_button.add_property('unlisted')
fin_button.warp_to(solar_fin_control)

class FinDisplay(Object):
    def describe(self):
        if solar_fin.extended:
            pront('The solar fin is extended.')
        else:
            pront('The solar fin is retracted.')
        if bridge_socket.is_powered():
            pront('Bridge:       power online')
        else:
            pront('Bridge:       power offline')
        if solar_fin.extended:
            pront('Engine room:  power online')
        elif yellow_button.pressed:
            pront('Engine room:  emergency power only')
        else:
            pront('Engine room:  emergency power available')
        if antenna_socket.is_powered():
            pront('Antenna:      power online')
        else:
            pront('Antenna:      power offline')
        if fin_socket.is_powered():
            pront('Fin control:  power online')
        elif yellow_button.pressed:
            pront('Fin control:  emergency power only')
        else:
            pront('Fin control:  power offline')
        if cargo_socket.is_powered():
            pront('Cargo hold:   power online')
        else:
            pront('Cargo hold:   power offline')
        if airlock_socket.is_powered():
            pront('Airlock:      power online')
        else:
            pront('Airlock:      emergency power only')

fin_display = FinDisplay('display', 'display#fin', ['display', 'fin display', 'control', 'controls', 'panel', 'fin panel', 'display panel', 'status display'])
fin_display.warp_to(solar_fin_control)
fin_display.add_property('unlisted')
fin_display.add_property('anchored')

class Breach(Object):
    def i_o_check(self, v, d_o):
        if v is put and d_o is plate:
            pront('You hold the plate across the breach like a metallic bandage. Immediately the surface of the plate begins to meld with the hull, and after a few seconds, the two have fused and the breach is entirely sealed.')
            corridor2.set_description('This north-south corridor runs the length of the station. A branch to the east leads to the solar fin control room. A slightly discolored patch on one wall is all that remains of a meteor-induced hull breach.')
            plate.warp_to(offstage)
            breach.warp_to(offstage)
            stars.remove_loc(corridor2)
            inc_turn()
            return False
        return True

breach = Breach('breach', 'breach', ['breach', 'hull breach', 'hole', 'rend', 'perforation', 'puncture', 'gash'])
breach.warp_to(corridor2)
breach.set_description('Countless stars are visible through the breach in the hull. Unfortunately this breathtaking view must be covered up if the station atmosphere is to be restored.')
breach.add_property('unlisted')
breach.add_property('immobile')

crate = Container('supply crate', 'supply_crate', ['supply crate', 'crate', 'box', 'metal crate', 'metal box', 'metal supply crate', 'metal supply box', 'supply box'])
crate.warp_to(cargo_hold)
crate.add_property('openable')
crate.make_closed()
crate.set_description('A metal crate containing useful station supplies.')
crate.add_property('unlisted')
crate.set_bulk(150)

class PortableLamp(SuitTool):
    def get_brightness(self):
        if self in spacesuit.get_child_attachments() and power_cell in spacesuit.get_child_attachments() and power_cell.get_charge() > 0:
            return 2
        else:
            return 0

lamp = PortableLamp('lamp', 'lamp', ['lamp', 'lantern', 'flashlight', 'portable lamp', 'torch'])
lamp.warp_to(engineering)
lamp.set_description('A portable lamp that runs on an external power source and can be fitted to the wrist.')
lamp.add_property('initialize')
lamp.set_initial_description('A portable lamp lies discarded on the floor.')
lamp.set_allowed_parent_attachments([spacesuit])
spacesuit.add_allowed_child_attachment(lamp)
lamp.set_bulk(7)

welder = SuitTool('welder', 'welder', ['welder', 'space welder'])
welder.warp_to(crate)
welder.set_description('A special kind of welder that is built to work in the vacuum of deep space. It runs on an external power source and can be mounted to your wrist.')
welder.add_allowed_parent_attachment(spacesuit)
spacesuit.add_allowed_child_attachment(welder)

white_cable = Rope('white cable', 'white_cable', ['white cable', 'cable', 'white'])
white_cable.warp_to(crate)
white_cable.set_description('A short cable for transmitting electrical power. The ends of the cable can plug into standard sockets.')
white_cable.set_max_length(3)
white_cable.add_property('plug')
white_cable.set_bulk(7)

black_cable = Rope('black cable', 'black_cable', ['black cable', 'cable', 'black'])
black_cable.warp_to(crate)
black_cable.set_description('A long cable for transmitting electrical power. The ends of the cable can plug into standard sockets.')
black_cable.set_max_length(4)
black_cable.add_property('plug')
black_cable.set_bulk(8)

plate = Object('hull repair plate', 'hull_repair_plate', ['hull repair plate', 'plate', 'repair plate', 'metallic plate'])
plate.warp_to(crate)
plate.set_description('This unassuming metallic square has been specially formulated to fuse with titanium-ceramic on contact, allowing rapid repair of damaged surfaces.')
plate.set_bulk(15)

bunk = Bed('bunk', 'bunk', ['bunk', 'bed', 'my bed', 'my bunk'])
bunk.warp_to(quarters)
bunk.set_description('A bit of rest would be welcome right now, but the station repairs will have to come first.')
bunk.set_definite_article('your')
bunk.set_indefinite_article('your')
bunk.add_property('unlisted')

drawer = Container('drawer', 'drawer', ['drawer', 'pullout drawer'])
drawer.make_component_of(bunk)
drawer.add_property('openable')
drawer.make_closed()
drawer.set_description('The drawer provides a place to store your personal belongings.')

id_card = Object('identification card', 'identification_card', ['identification card', 'card', 'identification', 'i.d. card', 'id card', 'i.d.', 'id'])
id_card.warp_to(drawer)
id_card.set_description('This little card contains indentifying information about yourself, as well as security clearance and access permissions.')
id_card.set_definite_article('your')
id_card.set_indefinite_article('your')
slot.whitelist = [id_card]
id_card.set_bulk(1)

winch = Object('winch', 'winch', ['winch', 'pulley', 'windlass', 'electric winch', 'electric pulley', 'electric windlass'])
winch.warp_to(cargo_hold)
winch.add_property('anchored')
winch.add_property('unlisted')
winch.set_description('This electric winch is used to load cargo into the station. There is a power switch on one side which is used to reel in the attached cable.')

winch_switch = Object('power switch', 'power_switch', ['power switch', 'switch'])
winch_switch.make_component_of(winch)
winch_switch.set_description('A power switch that will reel in the winch when pressed.')

cable = Rope('metal cable', 'metal_cable', ['metal cable', 'cable', 'metal'])
cable.warp_to(cargo_hold)
cable.add_property('initialize')
cable.set_initial_description('A metal cable lies in a coil next to the winch; one end is tied to the winch\'s drum.')
cable.set_description('A metal cable that is used to move heavy cargo in conjunction with the winch.')
cable.set_max_length(3)
winch.add_allowed_child_attachment(cable)
cable.add_allowed_parent_attachment(winch)
cable.tie_to(winch)

rock = Object('chunk of rock', 'chunk_of_rock', ['chunk of rock', 'rock', 'chunk', 'meteor', 'meteorite', 'asteroid', 'fragment', 'rocky fragment', 'rocky meteor', 'rocky chunk'])
rock.warp_to(outer_hull_2)
rock.set_description('This fragment of a meteor has embedded itself into the solar fin extension mechanism, preventing it from operating.')
rock.add_property('custom_immobile')
rock.add_property('unlisted')
rock.set_custom_immobile_message('Despite your best efforts, the chunk of rock remains wedged in place.')

solar_fin = Object('solar fin', 'solar_fin', ['solar fin', 'fin', 'solar panel', 'panel', 'mechanism', 'extension mechanism'])
solar_fin.warp_to(outer_hull_2)
solar_fin.add_property('immobile')
solar_fin.add_property('unlisted')
solar_fin.set_description('The solar fin does not appear damaged, but the rock fragment is preventing it from extending.')
solar_fin.extended = False

antenna = Object('antenna', 'antenna', ['antenna', 'wire', 'wires'])
antenna.warp_to(outer_hull_3)
antenna.add_property('unlisted')
antenna.add_property('anchored')
antenna.set_description('Fortunately the delicate wires comprising the antenna appear undamaged.')

class Socket(Object):
    def __init__(self, name, id, synonyms):
        super().__init__(name, id, synonyms)
        self.powered = False
        self.set_allowed_child_attachments([white_cable, black_cable])
        white_cable.add_allowed_parent_attachment(self)
        black_cable.add_allowed_parent_attachment(self)
        self.add_property('anchored')
        self.add_property('unlisted')

    def set_power(self, v):
        assert type(v) == bool, 'The power status must be a boolean.'
        self.powered = v

    def is_powered(self):
        if self.powered:
            return True
        if white_cable in self.get_child_attachments():
            for x in white_cable.get_tied_objects():
                if isinstance(x, Socket) and x.powered:
                    return True
        if black_cable in self.get_child_attachments():
            for x in black_cable.get_tied_objects():
                if isinstance(x, Socket) and x.powered:
                    return True
        return False

    def describe(self):
        if self.is_powered():
            pront('A green light on the socket indicates the socket has power.')
        else:
            pront('A red light on the socket indicates the socket lacks power.')
        if white_cable in self.get_child_attachments() and black_cable in self.get_child_attachments():
            pront('A white cable and a black cable are plugged into it.')
        elif white_cable in self.get_child_attachments():
            pront('A white cable is plugged into it.')
        elif black_cable in self.get_child_attachments():
            pront('A black cable is plugged into it.')

airlock_socket = Socket('socket', 'socket#airlock', ['socket', 'power socket', 'light', 'red light', 'green light'])
airlock_socket.warp_to(airlock_exterior)

fin_socket = Socket('socket', 'socket#fin', ['socket', 'power socket', 'light', 'red light', 'green light'])
fin_socket.warp_to(solar_fin_control)

cargo_socket = Socket('socket', 'socket#cargo', ['socket', 'power socket', 'light', 'red light', 'green light'])
cargo_socket.warp_to(cargo_hold)

bridge_socket = Socket('socket', 'socket#bridge', ['socket', 'power socket', 'light', 'red light', 'green light'])
bridge_socket.warp_to(quarters)

antenna_socket = Socket('socket', 'socket#antenna', ['socket', 'power socket', 'light', 'red light', 'green light'])

antenna_axle = Object('drive axle', 'drive_axle', ['drive axle', 'axle', 'thin axle', 'thin metal axle', 'metal axle'])
antenna_axle.set_description('This thin metal axle controls the alignment of the antenna with the signal destination. At the moment it is broken in half, close to where it meets the motor.')
antenna_axle.broken = True

antenna_motor = Object('motor', 'motor', ['motor', 'electric motor', 'small motor', 'small electric motor'])
antenna_motor.set_description('This small electric motor drives the axle which, in turn, adjusts the antenna position.')

class AntennaPanel(Wrapper):
    def d_o_check(self, v):
        if (v == open or v == open2) and not self.is_open():
            self.make_open()
            antenna_socket.remove_property('hidden')
            antenna_axle.remove_property('hidden')
            antenna_motor.remove_property('hidden')
            pront('You tear off the panel cover and, in your haste, lose your grip on it. The cover floats away into the void, revealing a power socket, a small electric motor, and a drive axle. The drive axle is shorn in half, just above where it meets the motor.')
            inc_turn()
            return False
        return True

    def describe(self):
        if self.is_open():
            pront('A small compartment where the panel cover once sat contains a power socket, an electric motor, and a drive axle.')
        else:
            pront('The panel is closed at the moment.')

antenna_panel = AntennaPanel('panel', 'panel', ['panel', 'antenna panel', 'electronics panel', 'electronic panel', 'electric panel', 'cover', 'panel cover'])
antenna_panel.warp_to(outer_hull_3)
antenna_panel.add_property('unlisted')
antenna_panel.add_property('immobile')
antenna_panel.whitelist = []

antenna_motor.make_component_of(antenna_panel)
antenna_axle.make_component_of(antenna_panel)
antenna_socket.make_component_of(antenna_panel)

debris = Object('beam', 'beam', ['beam', 'support beam', 'collapsed beam', 'collapsed support beam', 'debris', 'collasped debris', 'fallen beam', 'support', 'fallen support', 'collapsed support', 'fallen debris', 'broken beam', 'broken support'])
debris.warp_to(corridor4)
debris.set_description('This fallen support is blocking the entrance to the living quarters. You will have to figure out how to move it if you want to get through.')
debris.add_property('unlisted')
debris.add_property('custom_immobile')
debris.set_custom_immobile_message('The support beam is far too large for you to even think about moving it by hand.')
debris.add_allowed_child_attachment(cable)
cable.add_allowed_parent_attachment(debris)

ducts = MultiObject('air ducts', 'air_ducts', ['air ducts', 'ducts', 'duct', 'air duct', 'vent', 'vents', 'air_vents'])
ducts.remove_property('distant')
ducts.set_loc_list([airlock, engineering, solar_fin_control, quarters, bridge, cargo_hold, corridor1, corridor2, corridor3, corridor4])
ducts.make_plural()
ducts.set_description('These air ducts distribute air around the station.')

systems = Object('essential systems', 'essential_systems', ['essential systems', 'systems', 'life support', 'power distribution'])
systems.add_property('unlisted')
systems.add_property('immobile')
systems.set_description('A tangle of pipes, valves, conduits, and all manner of other apparatus necessary to keep the station running.')
systems.warp_to(engineering)

stars = MultiObject('stars', 'stars', ['stars', 'star'])
stars.set_loc_list([corridor2, airlock_exterior, outer_hull_1, outer_hull_2, outer_hull_3])
stars.make_plural()
stars.set_description('Each of these pinpricks of light lies an almost unfathomable distance away from your tiny station.')

sun = MultiObject('sun', 'sun', ['sun', 'local sun'])
sun.set_description('Looking directly into the sun is a completely and utterly foolish idea.')
sun.set_loc_list([outer_hull_2, outer_hull_3])

class Monitor(Object):

    def generate_death(self):
        return choose(['was frozen to death by an ice iguana.', 'was incinerated by flaming swine.', 'was bludgeoned to a pulp by hyena-people.', 'died of dehydration.', 'died after contracting numerous fungal infections.', 'was stoned to death by baboons.', 'was telepathically hated to death by an irate brain wizard.', 'died after drinking asphalt.', 'died after drinking toxic sludge.', 'died after drinking lava.', 'died after drinking acid.', 'died after jumping into a hole of unknown depth that turned out to be actually quite deep.', 'was cut into small pieces by a saw-wielding robot.', 'was axed to death by a troll monarch.', 'died of gravitational collapse after eating gravitational collapse-inducing meatballs.', 'was gunned down by a group of turrets.', 'was assasinated by brain wizard-hunters after attempting to become a powerful brain wizard.', 'was impaled by a particularly spiteful plant lurking in ambush underfoot.', 'exploded after detonating a folding chair via sheer incompetence.', 'was killed on the spot by local authorities for asking the wrong questions.', 'spontaneously combusted.', 'died by violating the Pauli exclusion principle.'])

    def generate_name(self): #based on Etruscan phonology
        vowels = ["a","e","i","u"]
        syllabic_vowels = ["m","l","n","r"]
        consonants = ["p","ph","t","th","f","s","x","v","c","ch"]
        consonants_2 = ["ts","cs","tx","sp"]
        i=0
        while i < 50:
            name = ""
            selector = random.randint(1,10)
            if  selector < 5:
                name = name + consonants[random.randint(0,len(consonants) - 1)]
            elif selector < 8:
                name = name + vowels[random.randint(0,len(vowels) - 1)]
            elif selector < 10:
                name = name + syllabic_vowels[random.randint(0,len(syllabic_vowels) - 1)]
            else:
                name = name + consonants_2[random.randint(0,len(consonants_2) - 1)]
            j = random.randint(2,5)
            k = 0
            while k < j:
                selector = random.randint(1,10)
                if name[len(name)-1] in vowels:
                    if selector < 6:
                        name = name + consonants[random.randint(0,len(consonants) - 1)]
                    elif selector < 8:
                        name = name + syllabic_vowels[random.randint(0,len(syllabic_vowels) - 1)]
                    else:
                        name = name + consonants_2[random.randint(0,len(consonants_2) - 1)]
                elif name[len(name)-1] in consonants or name[len(name)-1] == "h":
                    if selector < 8:
                        name = name + vowels[random.randint(0,len(vowels) - 1)]
                    else:
                        name = name + syllabic_vowels[random.randint(0,len(syllabic_vowels) - 1)]
                else:
                    if selector < 4:
                        name = name + consonants[random.randint(0,len(consonants) - 1)]
                    elif selector < 5:
                        name = name + consonants_2[random.randint(0,len(consonants_2) - 1)]
                    else:
                        name = name + vowels[random.randint(0,len(vowels) - 1)]
                k += 1
            selector = random.randint(1,10)
            if (not (name[0] in vowels) and selector == 1):
                name = "o" + name
            selector = random.randint(1,10)
            if (not (name[len(name) - 1] in vowels) and selector == 1):
                name = name + "o"
            selector = random.randint(1,10)
            if (not (name[0] in consonants) and (name[0] != "o")) and (selector == 1):
                name = "h" + name
            if (not (name[len(name)-1] in vowels) and (name[len(name)-1] != "o")) and (name[len(name)-1] != "s"):
                name = name + vowels[random.randint(0,len(vowels) - 1)]
            return name


    def describe(self):
        name = self.generate_name().capitalize()
        death_method = self.generate_death()
        pront('This monitor is a welcome source of recreation in your spare time. Right now, it is replaying someone\'s livestream of the totally original game Caves of Quod, in which a series of adventurers die in bizarre ways while exploring the ruins of past civilizations. The latest casualty is the adventurer ' + name + ', who ' + death_method)

monitor = Monitor('video monitor', 'video_monitor', ['video monitor', 'monitor', 'quod', 'caves', 'cave', 'caves of quod'])
monitor.warp_to(quarters)
monitor.add_property('unlisted')
monitor.add_property('anchored')

class CellRechargeTrigger(Pulser):
    def engage(self):
        super().engage()
        if power_cell in charger.get_child_attachments() and power_cell.get_charge() < 36 and yellow_button.pressed:
            power_cell.set_charge(36)
            pront('The charger chimes twice.')
cell_recharge_trigger = CellRechargeTrigger()
cell_recharge_trigger.activate()

class AirRefillTrigger(Pulser):
    def engage(self):
        super().engage()
        if air_tank in pump.get_child_attachments() and air_tank.get_air() < 120 and yellow_button.pressed:
            air_tank.set_air(120)
            pront('You hear a brief hissing sound from the pump.')
air_refill_trigger = AirRefillTrigger()
air_refill_trigger.activate()

class Drainer(Pulser):
    def engage(self):
        super().engage()
        if not player.get_loc().get_atmosphere():
            if not 'worn' in spacesuit.get_properties():
                lose(0)
            elif air_tank not in spacesuit.get_child_attachments():
                lose(1)
            elif air_tank.get_air() <= 0:
                lose(2)
            else:
                air_tank.set_air(max(0, air_tank.get_air() - 3))
                if 23 <= air_tank.get_air() <= 25:
                    pront('You notice that your air supply is starting to become stale.')
                if 5 <= air_tank.get_air() <= 7:
                    pront('It has become very difficult to breathe.')
                if air_tank.get_air() == 0:
                    pront('Your air supply has run out. This could prove problematic.')
        if lamp in spacesuit.get_child_attachments() and power_cell in spacesuit.get_child_attachments() and power_cell.get_charge() > 0:
            power_cell.set_charge(max(0, power_cell.get_charge() - 2))
            if 5 <= power_cell.get_charge() <= 7:
                pront('The lamp blinks twice to alert you that it is low on power.')
            if power_cell.get_charge() == 0:
                pront('The lamp winks out as it depletes the last of the power cell\'s charge.')
drainer = Drainer()
drainer.activate()

class Break(Verb2):
    def body(self, d_o, i_o):
        if d_o is rock and i_o is drill:
            if power_cell in spacesuit.get_child_attachments() and drill in spacesuit.get_child_attachments() and power_cell.get_charge() > 0:
                d_o.warp_to(offstage)
                power_cell.set_charge(max(0, power_cell.get_charge() - 6))
                outer_hull_2.set_description('This part of the station is well lit because it faces the local sun. As such, it was the logical place to put the station\'s solar fin. The rock that was jamming the fin extension mechanism has been removed, and the fin is ready to be extended. Handholds here lead up and down.')
                solar_fin.set_description("The rock that was jamming the fin extension mechanism has been removed, and the fin is ready to be extended.")
                pront('You fire up the drill and press it against the rock. Within moments, it breaks apart, freeing the solar fin.')
                inc_turn()
            else:
                pront('The drill needs power to be used for drilling.')
        elif d_o is debris and i_o is drill:
            pront('Tough as the drill bit is, a titanium-ceramic beam of this size is far too much for it to handle.')
        elif d_o is rock:
            pront(f'{i_o.art_d().capitalize()} is not well-suited to breaking rocks.')
        elif d_o is debris:
            pront('It would take nothing short of another meteor impact to break the beam in two.')
        elif i_o is drill:
            pront(f'{d_o.art_d().capitalize()} is not something that should be drilled.')
        else:
            pront(f'{i_o.art_d().capitalize()} is not much use for breaking things, and it would be a bad idea to break {d_o.art_d()} anyways.')

break2 = Break('break_with', ['break', 'destroy', 'smash', 'pulverize', 'attack', 'crush', 'shatter', 'smite', 'drill'], ('with', 'using'))

class DrillV(Verb1):
    def body(self, d_o):
        if not drill.is_visible():
            pront('You cannot drill anything without a drill.')
        else:
            break2.body(d_o, drill)

drillv = DrillV('drill', ['drill'])


class Cover(Verb2):
    def body(self, d_o, i_o):
        if d_o is breach and i_o is plate:
            fix.body(d_o, i_o)
        else:
            pront(f'You cannot cover {d_o.art_d()} with {i_o.art_d()}.')

cover = Cover('cover_with', ['cover', 'seal', 'block', 'occlude'], ('with', 'using'))

class Fix(Verb2):
    def body(self, d_o, i_o):
        if d_o not in [breach, antenna_axle]:
            pront(f'{d_o.art_d().capitalize()} is not in need of repair.')
        elif i_o not in [welder, plate]:
            pront(f'{i_o.art_d().capitalize()} is a poor choice of repair tool.')
        elif d_o is breach:
            if i_o is welder:
                pront('The breach is far too large to repair with a welder.')
            else:
                plate.warp_to(offstage)
                breach.warp_to(offstage)
                corridor2.set_description('This north-south corridor runs the length of the station. A branch to the east leads to the solar fin control room. A slightly discolored patch on one wall is all that remains of a meteor-induced hull breach.')
                pront('You hold the plate across the breach like a metallic bandage. Immediately the surface of the plate begins to meld with the hull, and after a few seconds, the two have fused and the breach is entirely sealed.')
                inc_turn()
        else:
            if not antenna_axle.broken:
                pront('The axle has already been repaired.')
            elif i_o is plate:
                pront('The repair plate is much too large to be of use repairing a small axle like this one.')
            else:
                if power_cell in spacesuit.get_child_attachments() and welder in spacesuit.get_child_attachments() and power_cell.get_charge() > 0:
                    antenna_axle.broken = False
                    power_cell.set_charge(max(0, power_cell.get_charge() - 6))
                    antenna_axle.set_description('This thin metal axle controls the alignment of the antenna with the signal destination. You can see a seam where it has been broken and welded back together.')
                    pront('You spot weld the two halves of the axle together. The weld is not the cleanest, but it will hold until you can call in a proper repair crew to replace the part.')
                    inc_turn()
                else:
                    pront('The welder needs to be powered before repairs can be attemped.')

fix = Fix('repair_with', ['repair', 'fix', 'mend', 'restore', 'patch', 'weld'], ('with','using'))

class Flip(Verb1):
    def body(self, d_o):
        if d_o is winch_switch or lever:
            push.body(d_o)
        else:
            pront(f'You cannot flip {d_o.art_d()}.')
flip = Flip('flip', ['flip', 'flick'])

class Slide(Verb2):
    def body(self, d_o, i_o):
        if d_o is id_card and i_o is slot:
            put.body(d_o, i_o)
        else:
            pront(f'You cannot slide {d_o.art_d()} through {i_o.art_d()}')
slide = Slide('slide_through', ['slide', 'swipe', 'drag'], ('through', 'into', 'across', 'in', 'on', 'onto'))

class Recharge(Verb1):
    def body(self, d_o):
        if d_o is not power_cell:
            pront(f'{d_o.art_d().capitalize()} is not something that can be recharged.')
        else:
            pront(f'You will need to attach the cell to a charger if you want to recharge it.')
recharge = Recharge('recharge', ['recharge', 'charge'])

class Refill(Verb1):
    def body(self, d_o):
        if d_o is not air_tank:
            pront(f'{d_o.art_d().capitalize()} is not something that can be refilled.')
        else:
            pront(f'You will need to attach the tank to a pump if you want to refill it.')
refill = Refill('refill', ['refill', 'fill'])

class Debug(Verb0):
    def body(self):
        player.warp_to(quarters)
        bridge_socket.powered = True
debug = Debug('debug', ['debug'])

class Look(Verb0):
    def body(self):
        player.get_loc().describe()
        player.know_objects_in_loc(player.get_loc())
        inc_turn()
look = Look('look_around', ['l','look','look around', 'stare', 'gaze'])

class Listen(Verb0):
    def body(self):
        player.get_loc().describe_sound()
        inc_turn()
listen = Listen('listen', ['listen', 'hear', 'hearken', 'harken'])

class Smell(Verb0):
    def body(self):
        player.get_loc().describe_smell()
        inc_turn()
smell = Smell('smell#', ['smell', 'sniff'])

class Wait(Verb0):
    def body(self):
        pront('You wait for a brief moment.')
        inc_turn()
wait = Wait('wait', ['wait', 'z'])

class Stand(Verb0):
    def body(self):
        if player.get_state() == 'standing':
            pront('You are already standing.')
        else:
            if hasattr(player, 'state_position'):
                if player.get_state() == 'standing atop something':
                    pront(f'You step down off of {player.get_state_position().art_d()}.')
                else:
                    pront(f'You stand up from {player.get_state_position().art_d()}.')
                player.reset_state()
            else:
                player.set_state('standing')
                pront('You stand up.')
            inc_turn()
stand = Stand('stand', ['stand', 'stand up', 'get up', 'get down', 'get off'])

class Sit(Verb0):
    def body(self):
        if player.get_state() == 'sitting':
            pront('You are already sitting.')
        else:
            if hasattr(player, 'state_position'):
                if 'sitting' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to sitting on {player.get_state_position().art_d()}.')
                    player.set_state('sitting')
                    inc_turn()
                else:
                    pront(f'You cannot sit on {player.get_state_position().art_d()}.')
            else:
                player.set_state('sitting')
                if player.get_state() == 'lying down':
                    pront('You sit up.')
                else:
                    pront('You sit down.')
                inc_turn()
sit = Sit('sit', ['sit', 'sit up', 'sit down'])

class Lie(Verb0):
    def body(self):
        if player.get_state() == 'lying down':
            pront('You are already lying down.')
        else:
            if hasattr(player, 'state_position'):
                if 'lying down' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to lying on {player.get_state_position().art_d()}.')
                    player.set_state('lying down')
                    inc_turn()
                else:
                    pront(f'You cannot lie on {player.get_state_position().art_d()}.')
            else:
                player.set_state('lying down')
                pront('You lie down.')
                inc_turn()
lie = Lie('lie', ['lie', 'lie down'])

class Quit(Verb0):
    def body(self):
        raise SystemExit(0)
quit = Quit('quit', ['quit'])

class Meme(Verb0):
    def body(self):
        pront('A hollow voice says, "Fool."')
        inc_turn()
meme = Meme('meme', ['git gud', 'bean', 'beans', 'borgar', 'shak', 'frie', 'hecc', 'meem', 'meme', 'it is wednesday, my dudes', 'duck', 'ducc', 'all birds are ducks', 'plugh', 'xyzzy', 'count leaves', 'kek', 'fr*ck', 'h*ck', 'finsh', 'fonsh', 'sheej', 'sheej tits', 'i hate sand', 'thicc', 'chungus', 'big chungus', 'waluigi', 'luigi', 'did you ever hear the tradgedy of darth plagueis the wise?', 'arma virumque cano', 'arma vivmqve cano', 'beef', 'beeves', 'b', 'leopards ate my face', 'embiggen', 'imbibe', 'succ', 'whomst', 'hewwo', '42', '69', '420', 'heck'])

class Blink(Verb0):
    def body(self):
        pront('You blink.')
        inc_turn()
blink = Blink('blink', ['blink', 'nictitate'])

class Help(Verb0):
    def body(self):
        pront('In this game, you can move in ten directions: north, south,' +
              ' west, east, northwest, northeast, southwest, southeast, up,' +
              ' and down. These commands can be abbreviated to "n," "s," "w,"' +
              ' "e," "nw," "ne," "sw," "se," "u," and "d." The command ' +
              '"inventory" (abbreviated "i") displays what your character is ' +
              'holding at the moment. The command "look" (abbreviated "l") ' +
              'gives you a view of your current location. Also useful is the ' +
              '"examine" command, or "x" for short. The "quit" command exits ' +
              'the game. This is not an exhaustive list: you may discover ' +
              'many other useful commands throughout the game. If you have ' +
              'an idea, don\'t be afraid to take a guess.')
help = Help('help', ['help','help me'])

class Hello(Verb0):
    def body(self):
        audience = False
        for x in player.get_loc().get_contents():
            if isinstance(x, NPC):
                if not audience:
                    audience = True
                    pront('You say "Hello."')
                if x.owngreetingPulser.get_activity():
                    x.greet_player()
                    x.owngreetingPulser.reactivate()
                    if x.ownwanderPulser.get_activity():
                        x.ownwanderPulser.reactivate()
                else:
                    pront(f'{x.art_d().capitalize()} does not respond.')
        if not audience:
            pront('You say "Hello," but notbody is there to respond.')
        inc_turn()
hello = Hello('hello', ['hello', 'hi', 'say hello', 'say hi'])

class Go_north(Verb0):
    def body(self):
        if 'n' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['n']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'n' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('n'):
                if 'n' in player.get_loc().get_exits():
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'n' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['n'])
go_north = Go_north('go_north', ['n', 'north', 'go north', 'walk north'])
go_north.set_required_states(['standing'])

class Go_south(Verb0):
    def body(self):
        if 's' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['s']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 's' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('s'):
                if 's' in player.get_loc().get_exits():
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 's' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['s'])
go_south = Go_south('go_south', ['s', 'south', 'go south', 'walk south'])
go_south.set_required_states(['standing'])

class Go_west(Verb0):
    def body(self):
        if 'w' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['w']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'w' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('w'):
                if 'w' in player.get_loc().get_exits():
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'w' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['w'])
go_west = Go_west('go_west', ['w', 'west', 'go west', 'walk west'])
go_west.set_required_states(['standing'])

class Go_east(Verb0):
    def body(self):
        if 'e' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['e']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'e' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('e'):
                if 'e' in player.get_loc().get_exits():
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'e' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['e'])
go_east = Go_east('go_east', ['e', 'east', 'go east', 'walk east'])
go_east.set_required_states(['standing'])

class Go_northwest(Verb0):
    def body(self):
        if 'nw' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['nw']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'nw' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('nw'):
                if 'nw' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['nw']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'nw' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['nw'])
go_northwest = Go_northwest('go_northwest', ['nw', 'northwest', 'go northwest', 'walk northwest'])
go_northwest.set_required_states(['standing'])

class Go_northeast(Verb0):
    def body(self):
        if 'ne' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['ne']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'ne' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('ne'):
                if 'ne' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['ne']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'ne' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['ne'])
go_northeast = Go_northeast('go_northeast', ['ne', 'northeast', 'go northeast', 'walk northeast'])
go_northeast.set_required_states(['standing'])

class Go_southwest(Verb0):
    def body(self):
        if 'sw' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['sw']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'sw' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('sw'):
                if 'sw' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['sw']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'sw' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['sw'])
go_southwest = Go_southwest('go_southwest', ['sw', 'southwest', 'go southwest', 'walk southwest'])
go_southwest.set_required_states(['standing'])

class Go_southeast(Verb0):
    def body(self):
        if 'se' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['se']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'se' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('se'):
                if 'se' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['se']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'se' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['se'])
go_southeast = Go_southeast('go_southeast', ['se', 'southeast', 'go southeast', 'walk southeast'])
go_southeast.set_required_states(['standing'])

class Go_up(Verb0):
    def body(self):
        if 'u' in player.get_loc().get_exits():
            temp = player.get_loc().get_exits()['u']
            if isinstance(temp[0], Room):
                dest = temp[0]
            else:
                dest = temp[0].get_connection().get_loc()
        if 'u' in player.get_loc().get_nexits() or not player.check_taut_ropes(dest):
            if player.get_loc().travelcheck('u'):
                if 'u' in player.get_loc().get_exits():
                    temp = player.get_loc().get_exits()['u']
                    if isinstance(temp[0], Room):
                        pront(temp[1])
                        player.warp_to(temp[0])
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        if temp[0].is_open():
                            pront(temp[1])
                            player.warp_to(temp[0].get_connection().get_loc())
                            player.get_loc().describe()
                            inc_turn()
                        else:
                            pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
                elif 'u' in player.get_loc().get_nexits():
                    pront(player.get_loc().get_nexits()['u'])
go_up = Go_up('go_up', ['u', 'up', 'go up'])
go_up.set_required_states(['standing'])

class Go_down(Verb0):
    def body(self):
        if player.get_loc().travelcheck('d'):
            if 'd' in player.get_loc().get_exits():
                temp = player.get_loc().get_exits()['d']
                if isinstance(temp[0], Room):
                    pront(temp[1])
                    player.warp_to(temp[0])
                    player.get_loc().describe()
                    inc_turn()
                else:
                    if temp[0].is_open():
                        pront(temp[1])
                        player.warp_to(temp[0].get_connection().get_loc())
                        player.get_loc().describe()
                        inc_turn()
                    else:
                        pront(f'{temp[0].art_d().capitalize()} {temp[0].pluralize("is")} closed.')
            elif 'd' in player.get_loc().get_nexits():
                pront(player.get_loc().get_nexits()['d'])
go_down = Go_down('go_down', ['d', 'down', 'go down'])
go_down.set_required_states(['standing'])

class Check_inventory(Verb0):
    def body(self):
        if len(player.get_carried()) == 0:
            pront('You are not carrying anything.')
        else:
            pront('You are carrying:')
            player.list_contents()
check_inventory = Check_inventory('check_inventory', ['i', 'inventory', 'check inventory', 'take inventory'])

class Get_all(Verb0):
    def body(self):
        temp = []
        for x in player.get_loc().get_contents():
            taketest = True
            if x.is_reachable():
                for y in ['custom_immobile', 'immobile', 'anchored', 'component', 'no_implicit_get']:
                    if y in x.get_properties():
                        taketest = False
                        break
                if isinstance(x, NPC) or isinstance(x, RopeTrail):
                    taketest = False
                if isinstance(x, Rope) and len(x.get_tied_objects()) > 1:
                    taketest = False
                if hasattr(x, 'parent_attachment'):
                    taketest = False
                if taketest:
                    temp.append(x)
        if len(temp) == 0:
            pront('There is nothing here that you can pick up.')
        else:
            for z in temp:
                if z.get_bulk() > player.get_capacity():
                    pront(f'{z.art_d().capitalize()} {z.pluralize("is")} too big to carry around.')
                elif z.get_bulk() + player.get_content_bulk() > player.get_capacity():
                    pront(f'You are carrying too much to be able to get {z.art_d()}.')
                else:
                    z.warp_to(player)
                    z.remove_property('initialize')
                    pront(f'You pick up {z.art_d()}.')
            inc_turn()
get_all = Get_all('get_all', ['get all', 'get everything', 'pick up all', 'pick up everything', 'take all', 'take everything', 'acquire all', 'acquire everything', 'grab all', 'grab everything', 'yoink all', 'yoink everything'])

class Drop_all(Verb0):
    def body(self):
        temp = []
        for x in player.get_contents():
            rope_test = (isinstance(x, Rope) and len(x.get_tied_objects()) > 1) or (isinstance(x, Rope) and len(x.get_tied_objects()) == 1 and x.get_tied_objects()[0].is_within(player))
            if not(('component' in x.get_properties() or 'player_anatomy' in x.get_properties()) or hasattr(x, 'parent_attachment')) and not rope_test:
                temp.append(x)
        if len(temp) == 0:
            pront('You are not holding anything at the moment.')
        else:
            for z in temp:
                z.warp_to(player.get_loc())
                pront(f'You drop {z.art_d()}.')
            inc_turn()
drop_all = Drop_all('drop_all', ['drop all', 'drop everything', 'put down all', 'put down everything'])

class Examine(Verb1):
    def body(self, d_o):
        if player.get_loc().is_illuminated():
            d_o.describe()
            inc_turn()
        else:
            if d_o.get_brightness() == 1:
                d_o.describe()
                inc_turn()
            else:
                pront(f'It is too dark to see {d_o.art_d()} clearly.')
examine = Examine('examine', ['x', 'examine', 'inspect', 'look at', 'check', 'gaze at', 'stare at', 'view', 'investigate', 'behold', 'what is'])
examine.set_requires_contact(False)

class Listen_to(Verb1):
    def body(self, d_o):
        if d_o.is_audible():
            d_o.describe_sound()
        else:
            pront('You hear nothing.')
        inc_turn()
listen_to = Listen_to('listen|to', ['hear', 'listen to', 'harken', 'hearken'])
listen_to.set_requires_contact(False)

class Smell1(Verb1):
    def body(self, d_o):
        if d_o.is_smellable():
            d_o.describe_smell()
        else:
            pront('You smell nothing.')
        inc_turn()
smell1 = Smell1('smell', ['smell', 'sniff'])
smell1.set_requires_contact(False)

class Taste(Verb1):
    def body(self, d_o):
        if d_o.is_tasteable():
            d_o.describe_taste()
            inc_turn()
        else:
            pront(f'You cannot taste {d_o.art_d()} because you cannot reach {obliquefy(d_o.get_pronoun())}.')
taste = Taste('taste', ['taste', 'lick'])
taste.set_requires_contact(False)

class Touch(Verb1):
    def body(self, d_o):
        if d_o.is_touchable():
            d_o.describe_touch()
            inc_turn()
        else:
            pront(f'You cannot touch {d_o.art_d()} because you cannot reach {obliquefy(d_o.get_pronoun())}.')
touch = Touch('touch', ['touch', 'feel', 'prod', 'poke', 'tap', 'stroke'])
touch.set_requires_contact(False)

class Get(Verb1):
    def body(self, d_o):
        if (isinstance(d_o, MultiObject) or (d_o.is_within(player.get_loc()) and (not d_o.get_loc() == (player)))) and d_o.is_reachable():
            if 'custom_immobile' in d_o.get_properties():
                pront(d_o.get_custom_immobile_message())
            elif 'immobile' in d_o.get_properties():
                pront(f'{d_o.art_d().capitalize()} cannot be moved.')
            elif 'anchored' in d_o.get_properties():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} anchored in place.')
            elif 'component' in d_o.get_properties():
                if d_o.is_plural():
                    pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                else:
                    pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
            elif isinstance(d_o, NPC):
                pront(f'{d_o.art_d().capitalize()} might object to that.')
            elif not isinstance(d_o, MultiObject) and isinstance(d_o.get_loc(), NPC) and 'proffered' not in d_o.get_properties():
                pront(f'{d_o.get_loc().art_d().capitalize()} might object to that.')
            elif isinstance(d_o, RopeTrail) and len(d_o.get_parent_rope().get_tied_objects()) > 1:
                if 'plug' in d_o.get_parent_rope().get_properties():
                    pront(f'You cannot pick up {d_o.get_parent_rope().art_d()} while {d_o.get_parent_rope().get_pronoun()} {d_o.get_parent_rope().pluralize("is")} plugged in at both ends.')
                else:
                    pront(f'You cannot pick up {d_o.get_parent_rope().art_d()} while {d_o.get_parent_rope().get_pronoun()} {d_o.get_parent_rope().pluralize("is")} tied at both ends.')
            elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 1:
                if 'plug' in d_o.get_properties():
                    pront(f'You cannot pick up {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged in at both ends.')
                else:
                    pront(f'You cannot pick up {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} tied at both ends.')
            elif d_o.get_bulk() > player.get_capacity():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} too big to carry around.')
            elif d_o.get_bulk() + player.get_content_bulk() > player.get_capacity():
                pront(f'You are carrying too much to be able to get {d_o.pluralize("that")}.')
            elif isinstance(d_o, RopeTrail):
                p = d_o.get_parent_rope()
                c = p.get_room_order().index(player.get_loc())
                p.set_room_order(p.get_room_order()[:c+1])
                p.warp_to(player)
                pront(f'You gather up {p.art_d()} and pick it up.')
            else:
                d_o.remove_property('initialize')
                if 'proffered' in d_o.get_properties() and isinstance(d_o.get_loc(), NPC):
                    pront(f'You take {d_o.art_d()} from {d_o.get_loc().art_d()}.')
                elif hasattr(d_o, 'parent_attachment'):
                    t = d_o.get_parent_attachment()
                    d_o.detach()
                    if 'plug' in d_o.get_properties():
                        pront(f'You unplug {d_o.art_d()} from {t.art_d()} and pick {obliquefy(d_o.get_pronoun())} up.')
                    else:
                        pront(f'You detach {d_o.art_d()} from {t.art_d()} and pick {obliquefy(d_o.get_pronoun())} up.')
                else:
                    pront(f'You pick up {d_o.art_d()}.')
                d_o.warp_to(player)
                inc_turn()
        elif d_o in player.get_contents():
            if 'player_anatomy' in d_o.get_properties():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already part of your own body.')
            elif 'component' in d_o.get_properties():
                if d_o.is_plural():
                    pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                else:
                    pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
            else:
                pront(f'You already have {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        for x in ['player_anatomy', 'component', 'custom_immobile', 'immobile', 'anchored']:
            if x in d_o.get_properties():
                priority -= 1
        if d_o in player.get_contents():
            priority -= 5
        if isinstance(d_o, NPC):
            priority -= 1
        return (d_o, priority)
get = Get('get', ['get', 'pick up', 'acquire', 'take', 'grab', 'yoink', 'hold', 'obtain'])

class Get_all_but(Verb1):
    def body(self, d_o):
        temp = []
        for x in player.get_loc().get_contents():
            taketest = True
            if x.is_reachable():
                for y in ['custom_immobile', 'immobile', 'anchored', 'component', 'no_implicit_get']:
                    if y in x.get_properties():
                        taketest = False
                        break
                if isinstance(x, NPC) or isinstance(x, RopeTrail):
                    taketest = False
                if hasattr(x, 'parent_attachment'):
                    taketest = False
                if isinstance(x, Rope) and len(x.get_tied_objects()) > 1:
                    taketest = False
                if taketest and (x != d_o):
                    temp.append(x)
        if len(temp) == 0:
            if d_o.is_reachable() and not(d_o.get_loc() == player):
                pront('There is nothing else here that you can pick up.')
            else:
                pront('There is nothing here that you can pick up.')
        else:
            for z in temp:
                if z.get_bulk() > player.get_capacity():
                    pront(f'{z.art_d().capitalize()} {z.pluralize("is")} too big to carry around.')
                elif z.get_bulk() + player.get_content_bulk() > player.get_capacity():
                    pront(f'You are carrying too much to be able to get {z.art_d()}.')
                else:
                    z.warp_to(player)
                    z.remove_property('initialize')
                    pront(f'You pick up {z.art_d()}.')
            inc_turn()
get_all_but = Get_all_but('get|all|but', ['get all but', 'get everything but', 'pick up all but', 'pick up everything but', 'take all but', 'take everything but', 'acquire all but', 'acquire everything but', 'grab all but', 'grab everything but', 'yoink all but', 'yoink everything but', 'get all except', 'get everything except', 'pick up all except', 'pick up everything except', 'take all except', 'take everything except', 'acquire all except', 'acquire everything except', 'grab all except', 'grab everything except', 'yoink all except', 'yoink everything except'])
get_all_but.set_requires_contact(False)

class Drop(Verb1):
    def body(self, d_o):
            if 'component' in d_o.get_properties() and d_o in player.get_contents():
                if d_o.is_plural():
                    pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                else:
                    pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
            elif hasattr(d_o, 'parent_attachment'):
                if 'plug' in d_o.get_properties():
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged into {d_o.get_parent_attachment().art_d()}.')
                else:
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} attached to {d_o.get_parent_attachment().art_d()}.')
            elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 1:
                if 'plug' in d_o.get_properties():
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged in at both ends.')
                else:
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} tied at both ends.')
            elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) == 1 and d_o.get_tied_objects()[0].is_within(player):
                if 'plug' in d_o.get_properties():
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged into {d_o.get_tied_objects()[0].art_d()}.')
                else:
                    pront(f'You cannot drop {d_o.art_d()} while {d_o.get_pronoun()} {d_o.pluralize("is")} tied to {d_o.get_tied_objects()[0].art_d()}.')
            elif 'player_anatomy' in d_o.get_properties():
                pront(f'You are unwilling to attempt separating {d_o.art_d()} from your own body.')
            elif d_o in player.get_contents():
                d_o.warp_to(player.get_loc())
                pront(f'You drop {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'You do not have {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if d_o in player.get_contents():
            priority += 5
        if 'component' in d_o.get_properties():
            priority -= 10
        if hasattr(d_o, 'parent_attachment'):
            priority -= 10
        if 'player_anatomy' in d_o.get_properties():
            priority -= 10
        return (d_o, priority)
drop = Drop('drop', ['drop', 'put down'])

class Drop_all_but(Verb1):
    def body(self, d_o):
        temp = []
        for x in player.get_contents():
            rope_test = (isinstance(x, Rope) and len(x.get_tied_objects()) > 1) or (isinstance(x, Rope) and len(x.get_tied_objects()) == 1 and x.get_tied_objects()[0].is_within(player))
            if not(('component' in x.get_properties() or 'player_anatomy' in x.get_properties()) or hasattr(x, 'parent_attachment')) and not rope_test:
                if x != d_o:
                    temp.append(x)
        if len(temp) == 0:
            if d_o.get_loc() == player:
                pront('You are not holding anything else at the moment.')
            else:
                pront('You are not holding anything at the moment.')
        else:
            for z in temp:
                z.warp_to(player.get_loc())
                pront(f'You drop {z.art_d()}.')
            inc_turn()
drop_all_but = Drop_all_but('drop|all|but', ['drop all but', 'drop everything but', 'put down all but', 'put down everything but', 'drop all except', 'drop everything except', 'put down all except', 'put down everything except'])
drop_all_but.set_requires_contact(False)

class Go_to(Verb1):
    def body(self, d_o):
        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already nearby. You could reach over and touch {d_o.art_d()} if you so wished.')
go_to = Go_to('go|to', ['approach', 'go to', 'go towards', 'move to', 'move towards', 'walk to', 'walk towards'])

class Turn(Verb1):
    def body(self, d_o):
        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be turned.')
turn = Turn('turn', ['turn', 'twist', 'crank', 'rotate'])

class Wear(Verb1):
    def body(self, d_o):
        if d_o.get_loc() == player:
            if 'clothing' in d_o.get_properties() and not 'worn' in d_o.get_properties():
                pront(f'You put on {d_o.art_d()}.')
                d_o.add_property('worn')
                inc_turn()
            elif 'worn' in d_o.get_properties():
                pront(f'You are already wearing {d_o.art_d()}.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be worn.')
        else:
            pront(f'You are not holding {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if d_o in player.get_contents() and 'clothing' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
wear = Wear('wear', ['wear', 'put on', 'slip on', 'equip', 'don'])

class TakeOff(Verb1):
    def body(self, d_o):
        if d_o.get_loc() == player:
            if 'worn' in d_o.get_properties():
                pront(f'You take off {d_o.art_d()}.')
                d_o.remove_property('worn')
                inc_turn()
            else:
                pront(f'You are not wearing {d_o.art_d()}.')
        else:
            pront(f'You are not in posession of {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if d_o in player.get_contents() and 'worn' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
take_off = TakeOff('take|off', ['doff', 'unequip', 'take off', 'slip off', 'divest myself of', 'divest me of'])

class Remove(Verb1):
    def body(self, d_o):
        if d_o.get_loc() == player and 'worn' in d_o.get_properties():
            take_off.body(d_o)
        else:
            detach.body(d_o)

    def prioritize(self, d_o):
        priority = 0
        if d_o in player.get_contents() and 'worn' in d_o.get_properties():
            priority += 5
        elif hasattr(d_o, 'parent_attachment') or (isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 0):
            priority += 5
        return (d_o, priority)
remove = Remove('remove', ['remove'])

class Enter(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Door) and 'enterable' in d_o.get_properties():
            if d_o.is_open():
                if not player.check_taut_ropes(d_o.get_connection().get_loc()):
                    pront(d_o.get_move_message())
                    player.warp_to(d_o.get_connection().get_loc())
                    player.get_loc().describe()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} closed.')
        else:
            pront(f'{d_o.art_d().capitalize()} cannot be entered.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'enterable' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority += 2
        return (d_o, priority)
enter = Enter('enter', ['enter', 'get in', 'go in', 'go into', 'walk in', 'walk into', 'move in', 'move into', 'climb in', 'climb into'])
enter.set_required_states(['standing'])

class Exit(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Door) and 'exitable' in d_o.get_properties():
            if d_o.is_open():
                if not player.check_taut_ropes(d_o.get_connection().get_loc()):
                    pront(d_o.get_move_message())
                    player.warp_to(d_o.get_connection().get_loc())
                    player.get_loc().describe()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} closed.')
        else:
            pront(f'{d_o.art_d().capitalize()} cannot be exited.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'exitable' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority += 2
        return (d_o, priority)
exit = Exit('exit', ['exit', 'get out of', 'walk out of', 'move out of', 'leave', 'climb out of'])
exit.set_required_states(['standing'])

class Go_through(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Door) and 'portal' in d_o.get_properties():
            if d_o.is_open():
                if not player.check_taut_ropes(d_o.get_connection().get_loc()):
                    pront(d_o.get_move_message())
                    player.warp_to(d_o.get_connection().get_loc())
                    player.get_loc().describe()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} closed.')
        else:
            pront(f'{d_o.art_d().capitalize()} cannot be entered.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'portal' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority += 2
        return (d_o, priority)
go_through = Go_through('go|through', ['go through', 'walk through', 'pass through', 'move through'])
go_through.set_required_states(['standing'])

class Climb_up(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Ladder) and d_o.leads_up():
            if not player.check_taut_ropes(d_o.get_up_destination()):
                pront(d_o.get_move_up_message())
                player.warp_to(d_o.get_up_destination())
                player.get_loc().describe()
                inc_turn()
        else:
            pront(f'You cannot climb up {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Ladder) and d_o.leads_up():
            priority += 5
        return (d_o, priority)
climb_up = Climb_up('climb|up', ['climb up', 'go up', 'walk up', 'travel up'])
climb_up.set_required_states(['standing'])

class Climb_down(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Ladder) and d_o.leads_down():
            if not player.check_taut_ropes(d_o.get_down_destination()):
                pront(d_o.get_move_down_message())
                player.warp_to(d_o.get_down_destination())
                player.get_loc().describe()
                inc_turn()
        else:
            pront(f'You cannot climb down {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Ladder) and d_o.leads_down():
            priority += 5
        return (d_o, priority)
climb_down = Climb_down('climb|down', ['climb down', 'go down', 'walk down', 'travel down'])
climb_down.set_required_states(['standing'])

class Climb(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Ladder) and d_o.leads_up():
            if not player.check_taut_ropes(d_o.get_up_destination()):
                pront(d_o.get_move_up_message())
                player.warp_to(d_o.get_up_destination())
                player.get_loc().describe()
                inc_turn()
        elif isinstance(d_o, Ladder) and d_o.leads_down():
            if not player.check_taut_ropes(d_o.get_down_destination()):
                pront(d_o.get_move_down_message())
                player.warp_to(d_o.get_down_destination())
                player.get_loc().describe()
                inc_turn()
        else:
            pront(f'You cannot climb {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Ladder) and (d_o.leads_up() or d_o.leads_down()):
            priority += 5
        return (d_o, priority)
climb = Climb('climb', ['climb'])
climb.set_required_states(['standing'])

class Open(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Container) and 'openable' in d_o.get_properties():
            if d_o.is_open():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
            else:
                if isinstance(d_o, Ampuole):
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} sealed.')
                elif d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} locked.')
                else:
                    if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                        pront(f'You open {d_o.art_d()}. In doing so, you reveal:')
                        d_o.make_open()
                        d_o.list_contents()
                    else:
                        pront(f'You open {d_o.art_d()}.')
                        d_o.make_open()
                    inc_turn()
        elif isinstance(d_o, Door) and 'openable' in d_o.get_properties():
            if d_o.is_open():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
            else:
                if d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} locked.')
                else:
                    d_o.make_open()
                    pront(f'You open {d_o.art_d()}.')
                    inc_turn()
        elif isinstance(d_o, Door):
            pront(f'You cannot open {d_o.art_d()}.')
        else:
            pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be opened.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'openable' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority -= 5
        if isinstance(d_o, Container) and 'openable' in d_o.get_properties():
            priority += 5
            if d_o.is_open():
                priority -= 5
        return (d_o, priority)
open = Open('open', ['open'])

class Close(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Container) and 'openable' in d_o.get_properties():
            if d_o.is_open():
                d_o.make_closed()
                pront(f'You close {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already closed.')
        elif isinstance(d_o, Door) and 'openable' in d_o.get_properties():
            if d_o.is_open():
                d_o.make_closed()
                pront(f'You close {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already closed.')
        else:
            pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be closed.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, Door) and 'openable' in d_o.get_properties():
            priority += 5
            if not d_o.is_open():
                priority -= 5
        if isinstance(d_o, Container) and 'openable' in d_o.get_properties():
            priority += 5
            if not d_o.is_open():
                priority -= 5
        return (d_o, priority)
close = Close('close', ['close', 'shut'])

class Lock(Verb1):
    def body(self, d_o):
        if isinstance(d_o, LockedDoor) and not isinstance(d_o, KeyedDoor):
            if d_o.is_locked():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already locked.')
            elif d_o.is_open():
                pront(f'{d_o.art_d().capitalize()} cannot be locked while {d_o.pluralize("it is")} open.')
            else:
                pront(f'You lock {d_o.art_d()}.')
                d_o.lock()
                if d_o.get_locklink():
                    d_o.get_connection().lock()
                inc_turn()
        else:
            if isinstance(d_o, KeyedDoor) or (isinstance(d_o, Locker) and not isinstance(d_o, Ampuole)):
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that you can lock by hand.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that you can lock.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, LockedDoor) and not isinstance(d_o, KeyedDoor):
            priority += 5
            if d_o.is_open() or d_o.is_locked():
                priority -= 5
        if isinstance(d_o, KeyedDoor) or (isinstance(d_o, Locker) and not isinstance(d_o, Ampuole)):
            priority +=1
            if d_o.is_open() or d_o.is_locked():
                priority -= 1
        return (d_o, priority)
lock = Lock('lock', ['lock'])

class Unlock(Verb1):
    def body(self, d_o):
        if isinstance(d_o, LockedDoor) and not isinstance(d_o, KeyedDoor):
            if not d_o.is_locked():
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already unlocked.')
            else:
                pront(f'You unlock {d_o.art_d()}.')
                d_o.unlock()
                if d_o.get_locklink():
                    d_o.get_connection().unlock()
                inc_turn()
        else:
            if isinstance(d_o, KeyedDoor) or (isinstance(d_o, Locker) and not isinstance(d_o, Ampuole)):
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that you can unlock by hand.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that you can unlock.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, LockedDoor) and not isinstance(d_o, KeyedDoor):
            priority += 5
            if not d_o.is_locked():
                priority -= 5
        if isinstance(d_o, KeyedDoor) or (isinstance(d_o, Locker) and not isinstance(d_o, Ampuole)):
            priority +=1
            if not d_o.is_locked():
                priority -= 1
        return (d_o, priority)
unlock = Unlock('unlock', ['unlock'])

class Shake(Verb1):
    def body(self, d_o):
        if d_o.get_loc() == player:
            if isinstance(d_o, Container) and not isinstance(d_o, Surface):
                if len(d_o.get_contents()) > 1:
                    pront(f'You hear some objects moving around inside {d_o.art_d()}.')
                elif len(d_o.get_contents()) == 1:
                    pront(f'You hear an object moving around inside {d_o.art_d()}.')
                else:
                    pront(f'Shaking {d_o.art_d()} does nothing.')
            elif isinstance(d_o, Surface) and len(d_o.get_contents()) > 0:
                name = []
                temp = []
                for x in d_o.get_contents():
                    temp.append(x)
                for y in temp:
                    name.append(y.art_d())
                    y.warp_to(player.get_loc())
                pront(f'You shake {d_o.art_d()}, causing ' + sequence(name, 'and') + ' to fall to the ground.')
            else:
                pront(f'Shaking {d_o.art_d()} does nothing.')
            inc_turn()
        else:
            pront(f'You are not holding {d_o.art_d()}.')
shake = Shake('shake', ['shake', 'wave', 'agitate', 'rattle'])

class Push(Verb1):
    def body(self, d_o):
        l1 = white_cable.get_room_order(); l2 = black_cable.get_room_order(); l3 = cable.get_room_order();
        if d_o is left_button:
            if exterior_airlock_door_1.is_open():
                pront('The display flashes a warning, telling you that you cannot open both airlock doors at the same time.')
            elif airlock.get_atmosphere() != corridor1.get_atmosphere():
                pront('The display flashes a warning, telling you that you cannot open the airlock door while the inside and outside pressures are not equal.')
            elif ((corridor1 in l1 and airlock in l1) or (corridor1 in l2 and airlock in l2)) or (corridor1 in l3 and airlock in l3):
                pront('The airlock door begins to close, but opens again after striking the cable. The display flashes a warning telling you to clear the airlock doorway of obstructions before closing the door.')
            else:
                if interior_airlock_door_1.is_open():
                    interior_airlock_door_1.make_closed()
                    pront('The interior airlock door slides shut.')
                else:
                    interior_airlock_door_1.make_open()
                    pront('The interior airlock door slides open.')
            inc_turn()
        elif d_o is right_button:
            if interior_airlock_door_1.is_open():
                pront('The display flashes a warning, telling you that you cannot open both airlock doors at the same time.')
            elif airlock.get_atmosphere() != airlock_exterior.get_atmosphere():
                pront('The display flashes a warning, telling you that you cannot open the airlock door while the inside and outside pressures are not equal.')
            elif ((airlock_exterior in l1 and airlock in l1) or (airlock_exterior in l2 and airlock in l2)) or (airlock_exterior in l3 and airlock in l3):
                pront('The airlock door begins to close, but opens again after striking the cable. The display flashes a warning telling you to clear the airlock doorway of obstructions before closing the door.')
            else:
                if exterior_airlock_door_1.is_open():
                    exterior_airlock_door_1.make_closed()
                    pront('The exterior airlock door slides shut.')
                else:
                    exterior_airlock_door_1.make_open()
                    pront('The exterior airlock door slides open.')
            inc_turn()
        elif d_o is lever:
            if (interior_airlock_door_1.is_open() or exterior_airlock_door_1.is_open()):
                if airlock.get_atmosphere():
                    pront('The display flashes a warning, telling you that you cannot depressurize the airlock while one of the doors is open.')
                else:
                    pront('The display flashes a warning, telling you that you cannot repressurize the airlock while one of the doors is open.')
            else:
                if airlock.get_atmosphere():
                    airlock.set_atmosphere(False)
                    pront('You hear a hissing sound as air is vented from the chamber.')
                else:
                    airlock.set_atmosphere(True)
                    pront('You hear a hissing sound as air is pumped into the chamber.')
            inc_turn()
        elif d_o is yellow_button:
            if yellow_button.pressed:
                pront('You press the yellow button again, but since emergency power is already on, nothing changes.')
            else:
                yellow_button.pressed = True
                pront('You press the yellow button and activate the emergency power reserves. The life support machinery hums as it comes back online, and both the power cell charger and the air pump beep to indicate they are operational.')
            inc_turn()
        elif d_o is green_button:
            if not yellow_button.pressed:
                pront('An error message appears on the display, telling you that life support cannot be restored without emergency power.')
            elif breach.get_loc() is corridor2:
                pront('An error message appears on the display, telling you that life support cannot be restored while there is a hull breach.')
            elif not engineering.get_atmosphere():
                for x in [corridor1, corridor2, corridor3, corridor4, engineering, cargo_hold, bridge, quarters, solar_fin_control, airlock]:
                    x.set_atmosphere(True)
                pront('You hear hissing from numerous air ducts as the station atmosphere is restored.')
            else:
                pront('An error message appears on the display, telling you that life support has been restored already.')
            inc_turn()
        elif d_o is fin_button:
            if solar_fin.extended:
                pront('An error message appears on the display, telling you that the fin is already extended.')
            elif not yellow_button.pressed:
                pront('You press the button but nothing happens. It seems that emergency power feed to the extension mechanism is inactive.')
            elif rock.get_loc() is outer_hull_2:
                if rock.is_known():
                    pront('You press the button and hear the extension servos straining against the rock to no avail.')
                else:
                    pront('You press the button and hear the extension servos straining, but the fin remains retracted. It must be jammed on the outside somehow.')
            else:
                fin_socket.set_power(True)
                airlock_socket.set_power(True)
                solar_fin.extended = True
                solar_fin.set_description('The solar fin is extended and supplying the station with power.')
                outer_hull_2.set_description('This part of the station is well lit because it faces the local sun. As such, it was the logical place to put the station\'s solar fin. The fin currently extends towards the sun, gathering energy and supplying it to the station as electrical power. Handholds here lead up and down.')
                pront('The servos whir as the fin extends out from the station. Main power is back, although distribution is spotty. It seems several conduits inside the hull were broken in the storm and will have to be bypassed.')
            inc_turn()
        elif d_o is winch_switch:
            if not cargo_socket.is_powered():
                pront('You push the switch but nothing happens. It seems the winch is not powered.')
            elif winch not in cable.get_tied_objects():
                pront('The winch turns in place, but the metal cable is not tied to it, so nothing happens.')
            elif len(cable.get_room_order()) <= 1:
                pront('The winch does nothing, since the metal cable is already reeled in.')
            elif len(cable.get_tied_objects()) == 1:
                cable.set_room_order([winch.get_loc()])
                cable.warp_to(winch.get_loc())
                pront('The winch turns and reels in the metal cable.')
            else:
                b = cable.get_tied_objects().copy()
                b.remove(winch)
                cable.set_room_order([winch.get_loc()])
                cable.warp_to(winch.get_loc())
                b[0].warp_to(winch.get_loc())
                debris.set_description('The beam lies on the floor of the cargo hold. The way to the living quarters is now clear.')
                corridor4.set_description('The main corridor terminates here, at the entrance to the living quarters. The way north is now clear, scrape marks on the floor being the only evidence of the fallen beam\'s former presence. The corridor stretches away to the south.')
                cargo_hold.set_description('This small cargo hold is where the station\'s supplies are stored. A crate sitting at the center of the room beckons your attention; there is also a winch bolted to the floor next to it. A power socket sits on the wall next to the start of the branch corridor, which leads east to the main corridor. The broken support beam lays beside the winch here, having been dragged clear of its former position in the corridor.')
                pront('The winch strains as it reels in the metal cable. Eventually the support beam is dragged into the cargo hold, accompanied by a horrific grating sound.')
        elif d_o is red_button:
            if not bridge_socket.is_powered():
                pront('You press the red button but nothing happens. It seems you need to restore power to the bridge before you can send a distress call.')
            elif not antenna_socket.is_powered():
                pront('An automated voice says: "Power to the antenna is currently offline. No transmissions can be sent until power is restored."')
            elif antenna_axle.broken:
                pront('An automated voice says: "The antenna alignment is unresponsive. Checking the integrity of the antenna motor and drive axle is recommended. No transmissions can be sent until the antenna can be aligned."')
            else:
                win(0)
            inc_turn()
        else:
            pront(f'You cannot push {d_o.art_d()}.')
push = Push('push', ['press', 'push'])

class Pull(Verb1):
    def body(self, d_o):
        if d_o is lever:
            if (interior_airlock_door_1.is_open() or exterior_airlock_door_1.is_open()):
                if airlock.get_atmosphere():
                    pront('The display flashes a warning, telling you that you cannot depressurize the airlock while one of the doors is open.')
                else:
                    pront('The display flashes a warning, telling you that you cannot repressurize the airlock while one of the doors is open.')
            else:
                if airlock.get_atmosphere():
                    airlock.set_atmosphere(False)
                    pront('You hear a hissing sound as air is vented from the chamber.')
                else:
                    airlock.set_atmosphere(True)
                    pront('You hear a hissing sound as air is pumped into the chamber.')
            inc_turn()
        else:
            pront(f'You cannot pull {d_o.art_d()}.')
pull = Pull('pull', ['pull', 'yank'])

class Eat(Verb1):
    def body(self, d_o):
        if 'edible' in d_o.get_properties():
            pront(f'You eat {d_o.art_d()}. {d_o.pluralize("It is")} tasty.')
            d_o.warp_to(offstage)
            inc_turn()
        else:
            pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} inedible.')

    def prioritize(self, d_o):
        priority = 0
        if 'edible' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
eat = Eat('eat', ['eat', 'bite', 'consume', 'ingest'])

class Read(Verb1):
    def body(self, d_o):
        if 'readable' in d_o.get_properties():
            if player.get_loc().is_illuminated() or d_o.get_brightness() == 1:
                pront(d_o.get_read_description())
                inc_turn()
            else:
                pront('It is too dark to read here.')
        else:
            pront(f'You cannot read {d_o.art_d()}.')
read = Read('read', ['read'])

class Turn_on(Verb1):
    def body(self, d_o):
        if 'lamp' in d_o.get_properties():
            if d_o.get_brightness() == 2:
                pront(f'{d_o.art_d().capitalize()} is already on.')
            else:
                d_o.set_brightness(2)
                pront(f'You turn on {d_o.art_d()}.')
                inc_turn()
        else:
            pront(f'You cannot turn on {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if 'lamp' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
turn_on = Turn_on('turn|on', ['turn on', 'activate', 'light'])

class Turn_off(Verb1):
    def body(self, d_o):
        if 'lamp' in d_o.get_properties():
            if d_o.get_brightness() == 2:
                d_o.set_brightness(0)
                pront(f'You turn off {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} is already off.')
        else:
            pront(f'You cannot turn on {d_o.art_d()}.')

    def prioritize(self, d_o):
        priority = 0
        if 'lamp' in d_o.get_properties():
            priority += 5
        return (d_o, priority)
turn_off = Turn_off('turn|off', ['turn off', 'deactivate', 'inactivate', 'unlight'])

class Untie(Verb1):
    def body(self, d_o):
        if isinstance(d_o, RopeTrail):
            d_o = d_o.get_parent_rope()
        if isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 0:
            if len(d_o.get_tied_objects()) > 1:
                if d_o.get_tied_objects()[0].is_visible() and d_o.get_tied_objects()[1].is_visible():
                    pront(f'You should specify whether you want to untie {d_o.art_d()} from {d_o.get_tied_objects()[0].art_d()} or from {d_o.get_tied_objects()[1].art_d()}.')
                elif d_o.get_tied_objects()[0].is_visible() or d_o.get_tied_objects()[1].is_visible():
                    if d_o.get_tied_objects()[0].is_visible():
                        t = d_o.get_tied_objects()[0]
                    else:
                        t = d_o.get_tied_objects()[1]
                    t.get_child_attachments().remove(d_o)
                    d_o.remove_tied_object(t)
                    if 'plug' in d_o.get_properties():
                        pront(f'You unplug {d_o.art_d()} from {t.art_d()}.')
                    else:
                        pront(f'You untie {d_o.art_d()} from {t.art_d()}.')
                    d_o.update_locations()
                    inc_turn()
                else:
                    pront(f'You cannot see {d_o.get_tied_objects()[0].art_d()} or {d_o.get_tied_objects()[1].art_d()}.')
            else:
                t = d_o.get_tied_objects()[0]
                t.get_child_attachments().remove(d_o)
                d_o.remove_tied_object(t)
                if len(d_o.get_room_order()) > 1:
                    if 'plug' in d_o.get_properties():
                        pront(f'You unplug {d_o.art_d()} from {t.art_d()} and gather it up.')
                    else:
                        pront(f'You untie {d_o.art_d()} from {t.art_d()} and gather it up.')
                    if d_o.find_ultimate_room() is not player.get_loc():
                        d_o.warp_to(player.get_loc())
                else:
                    if 'plug' in d_o.get_properties():
                        pront(f'You unplug {d_o.art_d()} from {t.art_d()}.')
                    else:
                        pront(f'You untie {d_o.art_d()} from {t.art_d()}.')
                d_o.update_locations()
                inc_turn()
        else:
            for x in d_o.get_child_attachments():
                if isinstance(x, Rope):
                    self.body(x)
                    break
            else:
                pront(f'{d_o.art_d().capitalize()} is not tied to anything.')

        def prioritize(self, d_o):
            priority = 0
            if isinstance(d_o, rope) and len(d_o.get_tied_objects()) > 0:
                priority += 5
            return (d_o, priority)
untie = Untie('untie', ['untie', 'unbind', 'untether'])

class Unplug(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Rope) or isinstance(d_o, RopeTrail):
            untie.body(d_o)
        else:
            if hasattr(d_o, 'parent_attachment') and 'plug' in d_o.get_properties():
                t = d_o.get_parent_attachment()
                d_o.detach()
                pront(f'You unplug {d_o.art_d()} from {t.art_d()}.')
                inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not plugged into anything.')

    def prioritize(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment') or (isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 0):
            priority += 3
        if 'plug' in d_o.get_properties():
            priority += 3
        return (d_o, priority)
unplug = Unplug('unplug', ['unplug'])

class Detach(Verb1):
    def body(self, d_o):
        if isinstance(d_o, Rope) or isinstance(d_o, RopeTrail):
            untie.body(d_o)
        elif hasattr(d_o, 'parent_attachment'):
            if 'plug' in d_o.get_properties():
                unplug.body(d_o)
            else:
                t = d_o.get_parent_attachment()
                d_o.detach()
                pront(f'You detach {d_o.art_d()} from {t.art_d()}.')
                inc_turn()
        else:
            pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not attached to anything.')

    def prioritize(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment'):
            priority += 3
        return (d_o, priority)
detach = Detach('detach', ['detach', 'disconnect', 'unfasten'])

class Stand_On(Verb1):
    def body(self, d_o):
        if 'ground' in d_o.get_properties():
            if hasattr(player, 'state_position') and player.get_state() == 'standing':
                pront(f'You step off {player.get_state_position().art_d()}.')
                player.reset_state()
                inc_turn()
            else:
                stand.body()
        elif (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            if player.get_state() == 'standing atop something':
                pront(f'You are already standing on {d_o.art_d()}.')
            else:
                if 'standing atop something' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to standing on {d_o.art_d()}.')
                    player.set_state('standing atop something')
                    inc_turn()
                else:
                    pront(f'You cannot stand on {d_o.art_d()}.')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if 'standing atop something' in d_o.get_allowed_states():
                pront(f'You stand on {d_o.art_d()}.')
                player.set_state('standing atop something')
                player.set_state_position(d_o)
                inc_turn()
            elif 'standing' in d_o.get_allowed_states():
                    pront(f'You stand on {d_o.art_d()}.')
                    player.set_state('standing')
                    player.set_state_position(d_o)
                    inc_turn()
            else:
                pront(f'You cannot stand on {d_o.art_d()}.')
stand_on = Stand_On('stand|on', ['stand on', 'stand on top of', 'stand atop', 'stand up on', 'stand up on top of', 'stand up atop'])

class Sit_On(Verb1):
    def body(self, d_o):
        if 'ground' in d_o.get_properties():
            player.reset_state()
            sit.body()
        elif (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            if player.get_state() == 'sitting':
                pront(f'You are already sitting on {d_o.art_d()}.')
            else:
                if 'sitting' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to sitting on {d_o.art_d()}.')
                    player.set_state('sitting')
                    inc_turn()
                else:
                    pront(f'You cannot sit on {d_o.art_d()}.')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if 'sitting' in d_o.get_allowed_states():
                pront(f'You sit on {d_o.art_d()}.')
                player.set_state('sitting')
                player.set_state_position(d_o)
                inc_turn()
            else:
                pront(f'You cannot sit on {d_o.art_d()}.')
sit_on = Sit_On('sit|on', ['sit on', 'sit up on', 'sit down on', 'sit atop', 'sit on top of', 'sit down on top of', 'sit down atop', 'sit in', 'sit down in'])

class Lie_On(Verb1):
    def body(self, d_o):
        if 'ground' in d_o.get_properties():
            player.reset_state()
            lie.body()
        elif (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            if player.get_state() == 'lying down':
                pront(f'You are already lying down on {d_o.art_d()}.')
            else:
                if 'lying down' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to lying down on {d_o.art_d()}.')
                    player.set_state('lying down')
                    inc_turn()
                else:
                    pront(f'You cannot lie down on {d_o.art_d()}.')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if 'lying down' in d_o.get_allowed_states():
                pront(f'You lie down on {d_o.art_d()}.')
                player.set_state('lying down')
                player.set_state_position(d_o)
                inc_turn()
            else:
                pront(f'You cannot lie down on {d_o.art_d()}.')
lie_on = Lie_On('lie|on', ['lie on', 'lie down on', 'lie on top of', 'lie atop', 'lie down on top of', 'lie down atop'])

class Ride(Verb1):
    def body(self, d_o):
        if (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            if player.get_state() == 'riding a vehicle':
                pront(f'You are already riding {d_o.art_d()}.')
            else:
                if 'riding a vehicle' in player.get_state_position().get_allowed_states():
                    pront(f'You switch to riding {d_o.art_d()}.')
                    player.set_state('riding a vehicle')
                    inc_turn()
                else:
                    pront(f'You cannot ride {d_o.art_d()}.')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if 'riding a vehicle' in d_o.get_allowed_states():
                pront(f'You ride {d_o.art_d()}.')
                player.set_state('riding a vehicle')
                player.set_state_position(d_o)
                inc_turn()
            else:
                pront(f'You cannot ride {d_o.art_d()}.')
ride = Ride('ride', ['ride', 'ride on', 'ride atop', 'board', 'mount'])

class Get_On(Verb1):
    def body(self, d_o):
        if (hasattr(player, 'state_position') and player.get_state_position() == d_o):
            pront(f'You are already on {d_o.art_d()}')
        elif hasattr(player, 'state_position') and player.get_state() != 'standing':
            pront(f'You should get off {player.get_state_position().art_d()} first.')
        else:
            if len(d_o.get_allowed_states()) > 0:
                u = d_o.get_default_state()
                player.set_state(u)
                player.set_state_position(d_o)
                if u == 'standing atop something' or u == 'standing':
                    pront(f'You stand on {d_o.art_d()}.')
                elif u == 'sitting':
                    pront(f'You sit on {d_o.art_d()}.')
                elif u == 'lying down':
                    pront(f'You lie down on {d_o.art_d()}.')
                elif u == 'riding a vehicle':
                    pront(f'You ride {d_o.art_d()}.')
                else:
                    pront(f'You get on {d_o.art_d()}.')
                inc_turn()
            else:
                pront(f'You cannot get on {d_o.art_d()}.')
get_on = Get_On('get|on', ['get on', 'get onto', 'get into'])

class Greet(Verb1):
    def body(self, d_o):
        if isinstance(d_o, NPC) and d_o.owngreetingPulser.get_activity():
            d_o.greet_player()
            d_o.owngreetingPulser.reactivate(); d_o.ownwanderPulser.reactivate()
        else:
            pront(f'{d_o.art_d().capitalize()} does not respond.')

    def prioritize(self, d_o):
        priority = 0
        if isinstance(d_o, NPC):
            priority += 5
        return (d_o, priority)
greet = Greet('greet', ['greet', 'say hello to', 'say hi to'])
greet.set_requires_contact(False)

class Talk_to(Verb1):
    def body(self, d_o):
        if isinstance(d_o, NPC):
            pront(f'You can try asking {obliquefy(d_o.get_pronoun())} about something, or telling {obliquefy(d_o.get_pronoun())} about something.')
        else:
            pront(f'{d_o.art_d().capitalize()} is an inanimate object and will not respond.')
talk_to = Talk_to('talk|to', ['talk to', 'talk with', 'speak to', 'speak with', 'converse with'])
talk_to.set_requires_contact(False)

class Put(Verb2):
    def body(self, d_o, i_o):
        if d_o.get_loc() == player:
            if 'ground' in i_o.get_properties():
                drop.body(d_o)
            elif isinstance(i_o, Container) and not isinstance(i_o, Player) and not isinstance(i_o, NPC):
                if hasattr(i_o, 'whitelist') and d_o not in i_o.whitelist:
                    pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} not designed to accomodate {d_o.art_d()}.')
                elif hasattr(i_o, 'blacklist') and d_o in i_o.blacklist:
                    pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} not designed to accomodate {d_o.art_d()}.')
                elif 'player_anatomy' in d_o.get_properties():
                    pront(f'You are unwilling to attempt separating {d_o.art_d()} from your own body.')
                elif 'component' in d_o.get_properties():
                    if d_o.is_plural():
                        pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                    else:
                        pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
                elif hasattr(d_o, 'parent_attachment'):
                    if d_o.is_plural():
                        pront(f'You cannot put {d_o.art_d()} anywhere while they are attached to {d_o.get_parent_attachment().art_d()}.')
                    else:
                        pront(f'You cannot put {d_o.art_d()} anywhere while it is attached to {d_o.get_parent_attachment().art_d()}.')
                elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 1:
                    if 'plug' in d_o.get_properties():
                        pront(f'You cannot put {d_o.art_d()} anywhere while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged in at both ends.')
                    else:
                        pront(f'You cannot put {d_o.art_d()} anywhere while {d_o.get_pronoun()} {d_o.pluralize("is")} tied at both ends.')
                elif isinstance(d_o, Rope) and len(d_o.get_tied_objects()) == 1 and d_o.get_tied_objects()[0].is_within(player):
                    if 'plug' in d_o.get_properties():
                        pront(f'You cannot put {d_o.art_d()} anywhere while {d_o.get_pronoun()} {d_o.pluralize("is")} plugged into {d_o.get_tied_objects()[0].art_d()}.')
                    else:
                        pront(f'You cannot put {d_o.art_d()} anywhere while {d_o.get_pronoun()} {d_o.pluralize("is")} tied to {d_o.get_tied_objects()[0].art_d()}.')
                else:
                    if d_o is i_o:
                        pront('You cannot put something inside itself.')
                    elif i_o.is_within(d_o):
                        pront('Topology forbids such actions.')
                    elif not i_o.is_open():
                        pront('You cannot put something inside a closed container.')
                    elif d_o.get_bulk() > i_o.get_capacity():
                        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} too big to fit in the {i_o.art_d()}.')
                    elif d_o.get_bulk() + i_o.get_content_bulk() > i_o.get_capacity():
                        pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} too full to accomodate {d_o.art_d()}.')
                    else:
                        d_o.warp_to(i_o)
                        if isinstance(i_o, Surface):
                            pront(f'You put {d_o.art_d()} on {i_o.art_d()}.')
                        else:
                            pront(f'You put {d_o.art_d()} inside {i_o.art_d()}.')
                        inc_turn()
            else:
                pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} not a container.')
        else:
            pront(f'You are not holding {d_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if d_o.get_loc() == player:
            priority += 2
        if 'component' in d_o.get_properties():
            priority -= 5
        if 'player_anatomy' in d_o.get_properties():
            priority -= 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(i_o, Container) and not isinstance(i_o, Player) and not isinstance(i_o, NPC):
            priority += 5
            if not i_o.is_open():
                priority -= 4
        return (i_o, priority)
put = Put('put_in', ['put', 'place'], ('in', 'into', 'on', 'inside'))

class Give(Verb2):
    def body(self, d_o, i_o):
        if d_o.get_loc() == player:
            if isinstance(i_o, NPC):
                if 'player_anatomy' in d_o.get_properties():
                    pront(f'You are unwilling to attempt separating {d_o.art_d()} from your own body.')
                elif 'component' in d_o.get_properties():
                    if d_o.is_plural():
                        pront(f'{d_o.art_d().capitalize()} are integral parts of {d_o.get_parent_object().art_d()} and cannot be removed.')
                    else:
                        pront(f'{d_o.art_d().capitalize()} is an integral part of {d_o.get_parent_object().art_d()} and cannot be removed.')
                else:
                    if d_o is i_o:
                        pront('You cannot put something inside itself.')
                    elif i_o.is_within(d_o):
                        pront('Topology forbids such actions.')
                    elif d_o.get_bulk() > i_o.get_capacity():
                        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} too big for {i_o.art_d()} to carry.')
                    elif d_o.get_bulk() + i_o.get_content_bulk() > i_o.get_capacity():
                        pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} carrying too much to hold {d_o.art_d()}.')
                    else:
                        if d_o in i_o.get_covets():
                            d_o.warp_to(i_o)
                            pront(f'You give {d_o.art_d()} to {i_o.art_d()}.')
                        elif d_o in i_o.get_show_responses() or d_o in i_o.get_show_event_triggers():
                            pront(f'{i_o.art_d().capitalize()} looks at {d_o.art_d()}, but does not take it.')
                            show.body(d_o, i_o)
                        else:
                            pront(f'{i_o.art_d().capitalize()} says "I don\'t want {d_o.art_d()}."')
                        inc_turn()
            else:
                pront(f'{i_o.art_d().capitalize()} {i_o.pluralize("is")} not a person.')
        else:
            pront(f'You are not holding {d_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if d_o.get_loc() == player:
            priority += 2
        if 'component' in d_o.get_properties():
            priority -= 5
        if 'player_anatomy' in d_o.get_properties():
            priority -= 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(i_o, NPC):
            priority += 5
        return (i_o, priority)
give = Give('give_to', ['give', 'hand', 'donate', 'relinquish', 'offer'], ('to',))

class Open2(Verb2):
    def body(self, d_o, i_o):
        if i_o.get_loc() == player:
            if isinstance(d_o, Locker) and 'openable' in d_o.get_properties():
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if i_o in d_o.get_keylist():
                        if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                            pront(f'You open {d_o.art_d()} with {i_o.art_d()}. In doing so, you reveal:')
                            d_o.unlock()
                            d_o.make_open()
                            d_o.list_contents()
                        else:
                            pront(f'You open {d_o.art_d()} with {i_o.art_d()}.')
                            d_o.unlock()
                            d_o.make_open()
                        inc_turn()
                    elif i_o == hands and not d_o.is_locked():
                        if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                            pront(f'You open {d_o.art_d()}. In doing so, you reveal:')
                            d_o.make_open()
                            d_o.list_contents()
                        else:
                            pront(f'You open {d_o.art_d()}.')
                            d_o.make_open()
                        inc_turn()
                    else:
                        pront(f'You cannot open {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, Container) and ('openable' in d_o.get_properties()) and (i_o == hands):
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                        pront(f'You open {d_o.art_d()}. In doing so, you reveal:')
                        d_o.make_open()
                        d_o.list_contents()
                    else:
                        pront(f'You open {d_o.art_d()}.')
                        d_o.make_open()
                    inc_turn()
            elif isinstance(d_o, Container) and ('openable' in d_o.get_properties()):
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if (not d_o.is_transparent()) and len(d_o.get_contents()) > 0:
                        pront(f'After a brief period of contemplation, you realize that {i_o.art_d()} {i_o.pluralize("is")} unnecessary. Instead, you open {d_o.art_d()} with your hands. In doing so, you reveal:')
                        d_o.make_open()
                        d_o.list_contents()
                    else:
                        pront(f'After a brief period of contemplation, you realize that {i_o.art_d()} {i_o.pluralize("is")} unnecessary. Instead, you open {d_o.art_d()} with your hands.')
                        d_o.make_open()
                    inc_turn()
            elif isinstance(d_o, KeyedDoor):
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You open {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.unlock()
                        if d_o.get_locklink():
                            d_o.get_connection().unlock()
                        d_o.make_open()
                        inc_turn()
                    else:
                        pront(f'You cannot open {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, LockedDoor):
                if d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already open.')
                else:
                    if i_o == hands:
                        pront(f'You open {d_o.art_d()}.')
                    else:
                        pront(f'You briefly consider attempting to open {d_o.art_d()} with {i_o.art_d()}, but since the locking mechanism is designed to be operated by hand, you settle for doing that instead.')
                    d_o.unlock()
                    if d_o.get_locklink():
                        d_o.get_connection().unlock()
                    d_o.make_open()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be opened.')
        else:
            pront(f'You do not have {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, Door) or isinstance(d_o, Container):
            priority += 3
            if d_o.is_open():
                priority -= 5
            if 'openable' in d_o.get_properties():
                priority += 2
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if i_o.get_loc() == player:
            priority += 1
        return (i_o, priority)
open2 = Open2('open_with', ['open'], ('with', 'using'))

class Unlock2(Verb2):
    def body(self, d_o, i_o):
        if i_o.get_loc() == player:
            if isinstance(d_o, Locker) and not isinstance(d_o, Ampuole):
                if not d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already unlocked.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You unlock {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.unlock()
                        inc_turn()
                    else:
                        pront(f'You cannot unlock {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, KeyedDoor):
                if not d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already unlocked.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You unlock {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.unlock()
                        if d_o.get_locklink():
                            d_o.get_connection().unlock()
                        inc_turn()
                    else:
                        pront(f'You cannot unlock {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, LockedDoor):
                if not d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already unlocked.')
                else:
                    if i_o == hands:
                        pront(f'You unlock {d_o.art_d()}.')
                    else:
                        pront(f'You briefly consider attempting to unlock {d_o.art_d()} with {i_o.art_d()}, but since the locking mechanism is designed to be operated by hand, you settle for doing that instead.')
                    d_o.unlock()
                    if d_o.get_locklink():
                        d_o.get_connection().unlock()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be unlocked.')
        else:
            pront(f'You do not have {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, Door) or isinstance(d_o, Container):
            priority += 3
            if d_o.is_locked():
                priority -= 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if i_o.get_loc() == player:
            priority += 1
        return (i_o, priority)
unlock2 = Unlock2('unlock_with', ['unlock'], ('with', 'using'))

class Lock2(Verb2):
    def body(self, d_o, i_o):
        if i_o.get_loc() == player:
            if isinstance(d_o, Locker) and not isinstance(d_o, Ampuole):
                if d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already locked.')
                elif d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} cannot be locked while {d_o.pluralize("it is")} open.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You lock {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.lock()
                        inc_turn()
                    else:
                        pront(f'You cannot lock {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, KeyedDoor):
                if d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already locked.')
                elif d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} cannot be locked while {d_o.pluralize("it is")} open.')
                else:
                    if i_o in d_o.get_keylist():
                        pront(f'You lock {d_o.art_d()} with {i_o.art_d()}.')
                        d_o.lock()
                        if d_o.get_locklink():
                            d_o.get_connection().lock()
                        inc_turn()
                    else:
                        pront(f'You cannot lock {d_o.art_d()} with {i_o.art_d()}.')
            elif isinstance(d_o, LockedDoor):
                if d_o.is_locked():
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} already locked.')
                elif d_o.is_open():
                    pront(f'{d_o.art_d().capitalize()} cannot be locked while {d_o.pluralize("it is")} open.')
                else:
                    if i_o == hands:
                        pront(f'You lock {d_o.art_d()}.')
                    else:
                        pront(f'You briefly consider attempting to lock {d_o.art_d()} with {i_o.art_d()}, but since the locking mechanism is designed to be operated by hand, you settle for doing that instead.')
                    d_o.lock()
                    if d_o.get_locklink():
                        d_o.get_connection().lock()
                    inc_turn()
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not something that can be locked.')
        else:
            pront(f'You do not have {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, Door) or isinstance(d_o, Container):
            priority += 3
            if not d_o.is_locked():
                priority -= 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if i_o.get_loc() == player:
            priority += 1
        return (i_o, priority)
lock2 = Lock2('lock_with', ['lock'], ('with', 'using'))

class Tie(Verb2):
    def body(self, d_o, i_o):
        if d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments():
            self.body(i_o, d_o)
        else:
            if d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments() and isinstance(d_o, Rope):
                l = d_o.get_tied_objects()
                if len(d_o.get_tied_objects()) > 2:
                    if 'plug' in d_o.get_properties():
                        pront(f'{d_o.art_d().capitalize()} is already plugged into {l[0].art_d()} and {l[1].art_d()}.')
                    else:
                        pront(f'{d_o.art_d().capitalize()} is already tied to {l[0].art_d()} and {l[1].art_d()}.')
                else:
                    d_o.tie_to(i_o)
                    if 'plug' in d_o.get_properties():
                        pront(f'You plug {d_o.art_d()} into {i_o.art_d()}.')
                    else:
                        pront(f'You tie {d_o.art_d()} to {i_o.art_d()}.')
                    inc_turn()
            else:
                if 'plug' in d_o.get_properties() and isinstance(d_o, Rope):
                    pront(f'You cannot plug {d_o.art_d()} into {i_o.art_d()}.')
                else:
                    pront(f'You cannot tie {d_o.art_d()} to {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, Rope):
            priority += 2
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if (d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments()) or (d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments()):
            priority += 5
        return (i_o, priority)
tie = Tie('tie_to', ['tie', 'bind', 'tether'], ('to', 'onto'))

class Plug(Verb2):
    def body(self, d_o, i_o):
        if d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments():
            self.body(i_o, d_o)
        else:
            if d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments() and 'plug' in d_o.get_properties():
                if isinstance(d_o, Rope):
                    tie.body(d_o, i_o)
                else:
                    if d_o in i_o.get_child_attachments():
                        pront(f'{d_o.art_d().capitalize()} is already plugged into {i_o.art_d()}.')
                    else:
                        if hasattr(d_o, 'parent_attachment'):
                            pront(f'You unplug {d_o.art_d()} from {d_o.get_parent_attachment().art_d()} and plug {obliquefy(d_o.get_pronoun())} into {i_o.art_d()}.')
                        else:
                            pront(f'You plug {d_o.art_d()} into {i_o.art_d()}.')
                        d_o.attach_to(i_o)
                        inc_turn()
            else:
                pront(f'You cannot plug {d_o.art_d()} into {i_o.art_d()}.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if 'plug' in d_o.get_properties():
            priority += 2
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if (d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments()) or (d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments()):
            priority += 5
        return (i_o, priority)
plug = Plug('plug_into', ['plug'], ('into',))

class Attach(Verb2):
    def body(self, d_o, i_o):
        if d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments():
            self.body(i_o, d_o)
        else:
            if d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments():
                if 'plug' in d_o.get_properties():
                    plug.body(d_o, i_o)
                elif isinstance(d_o, Rope):
                    tie.body(d_o, i_o)
                else:
                    if d_o in i_o.get_child_attachments():
                        pront(f'{d_o.art_d().capitalize()} is already attached to {i_o.art_d()}.')
                    else:
                        if hasattr(d_o, 'parent_attachment'):
                            pront(f'You detach {d_o.art_d()} from {d_o.get_parent_attachment().art_d()} and attach {obliquefy(d_o.get_pronoun())} to {i_o.art_d()}.')
                        else:
                            pront(f'You attach {d_o.art_d()} to {i_o.art_d()}.')
                        d_o.attach_to(i_o)
                        inc_turn()
            else:
                pront(f'You cannot attach {d_o.art_d()} to {i_o.art_d()}.')

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if (d_o in i_o.get_allowed_child_attachments() and i_o in d_o.get_allowed_parent_attachments()) or (d_o in i_o.get_allowed_parent_attachments() and i_o in d_o.get_allowed_child_attachments()):
            priority += 5
        return (i_o, priority)
attach = Attach('attach_to', ['attach', 'connect', 'fasten'], ('to',))

class Untie2(Verb2):
    def body(self, d_o, i_o):
        if isinstance(d_o, RopeTrail):
            d_o = d_o.get_parent_rope()
        if isinstance(i_o, RopeTrail):
            i_o = i_o.get_parent_rope()
        if isinstance(i_o, Rope) and i_o in d_o.get_child_attachments():
            self.body(i_o, d_o)
        else:
            if isinstance(d_o, Rope) and len(d_o.get_tied_objects()) > 0:
                if d_o in i_o.get_child_attachments():
                    i_o.get_child_attachments().remove(d_o)
                    d_o.remove_tied_object(i_o)
                    if len(d_o.get_room_order()) > 1 and len(d_o.get_tied_objects()) == 0:
                        if 'plug' in d_o.get_properties():
                            pront(f'You unplug {d_o.art_d()} from {i_o.art_d()} and gather it up.')
                        else:
                            pront(f'You untie {d_o.art_d()} from {i_o.art_d()} and gather it up.')
                        if d_o.find_ultimate_room() is not player.get_loc():
                            d_o.warp_to(player.get_loc())
                    else:
                        if 'plug' in d_o.get_properties():
                            pront(f'You unplug {d_o.art_d()} from {i_o.art_d()}.')
                        else:
                            pront(f'You untie {d_o.art_d()} from {i_o.art_d()}.')
                    d_o.update_locations()
                    inc_turn()
                else:
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not tied to {i_o.art_d()}.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not tied to anything.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment'):
            priority += 3
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if d_o in i_o.get_child_attachments():
            priority += 5
        return (i_o, priority)
untie2 = Untie2('untie_from', ['untie', 'unbind', 'untether'], ('from',))

class Unplug2(Verb2):
    def body(self, d_o, i_o):
        if hasattr(i_o, 'parent_attachment') and i_o.get_parent_attachment() == d_o and 'plug' in i_o.get_properties():
            self.body(i_o, d_o)
        else:
            if isinstance(d_o, Rope) or isinstance(d_o, RopeTrail):
                untie2.body(d_o, i_o)
            elif hasattr(d_o, 'parent_attachment') and 'plug' in d_o.get_properties():
                if d_o in i_o.get_child_attachments():
                    d_o.detach()
                    pront(f'You unplug {d_o.art_d()} from {i_o.art_d()}.')
                    inc_turn()
                else:
                    pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not plugged into {i_o.art_d()}.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not plugged into anything.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment'):
            priority += 3
        if 'plug' in d_o.get_properties():
            priority += 3
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if d_o in i_o.get_child_attachments():
            priority += 5
        return (i_o, priority)
unplug2 = Unplug2('unplug_from', ['unplug'], ('from',))

class Detach2(Verb2):
    def body(self, d_o, i_o):
        if hasattr(i_o, 'parent_attachment') and i_o.get_parent_attachment() == d_o:
            self.body(i_o, d_o)
        else:
            if isinstance(d_o, Rope) or isinstance(d_o, RopeTrail):
                untie2.body(d_o, i_o)
            elif hasattr(d_o, 'parent_attachment'):
                if 'plug' in d_o.get_properties():
                    unplug2.body(d_o, i_o)
                else:
                    if d_o in i_o.get_child_attachments():
                        d_o.detach()
                        pront(f'You detach {d_o.art_d()} from {i_o.art_d()}.')
                        inc_turn()
                    else:
                        pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not attached to {i_o.art_d()}.')
            else:
                pront(f'{d_o.art_d().capitalize()} {d_o.pluralize("is")} not attached to anything.')

    def prioritize_d_o(self, d_o):
        priority = 0
        if hasattr(d_o, 'parent_attachment'):
            priority += 3
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if d_o in i_o.get_child_attachments():
            priority += 5
        return (i_o, priority)
detach2 = Detach2('detach_from', ['detach', 'remove', 'disconnect', 'unfasten'], ('from',))

class Ask(Verb2):
    def body(self, d_o, i_o):
        if isinstance(d_o, NPC):
            if i_o.is_known():
                if i_o in d_o.get_ask_responses():
                    q = d_o.get_ask_responses()[i_o]
                    r = q[0]
                    if q[1]:
                        r = '"' + r + '"'
                    pront(r)
                    for x in q[2]:
                        x.make_known()
                elif i_o in d_o.get_ask_event_triggers():
                    d_o.do_ask_event(i_o)
                else:
                    pront(f'"{d_o.get_unknown_ask_msg()}"')
            else:
                pront(f'You have not seen any {i_o.get_name()}.')
            if d_o.owngreetingPulser.get_activity():
                d_o.owngreetingPulser.reactivate()
            if d_o.ownwanderPulser.get_activity():
                d_o.ownwanderPulser.reactivate()
        else:
            pront(f'{d_o.art_d().capitalize()} is an inanimate object and does not respond.')
        inc_turn()

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, NPC):
            priority += 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(d_o, NPC):
            if i_o.is_known():
                priority += 4
            else:
                priority -=8
            if i_o in d_o.get_ask_responses() or i_o in d_o.get_ask_event_triggers():
                priority += 3
            else:
                priority -= 6
        else:
            priority -= 1
        return (i_o, priority)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        if len(new) > 1 and num <= 0:
            return [new[0]]
        return new
ask = Ask('ask_about', ['ask', 'interrogate', 'query'], ('about',))
ask.set_d_o_requires_contact(False)
ask.set_i_o_requires_contact(False)
ask.set_i_o_requires_sight(False)

class Tell(Verb2):
    def body(self, d_o, i_o):
        if isinstance(d_o, NPC):
            if i_o.is_known():
                if i_o in d_o.get_tell_responses():
                    q = d_o.get_tell_responses()[i_o]
                    r = q[0]
                    if q[1]:
                        r = '"' + r + '"'
                    pront(r)
                    for x in q[2]:
                        x.make_known()
                elif i_o in d_o.get_tell_event_triggers():
                    d_o.do_tell_event(i_o)
                else:
                    pront(f'"{d_o.get_unknown_tell_msg()}"')
            else:
                pront(f'You have not seen any {i_o.get_name()}.')
            if d_o.owngreetingPulser.get_activity():
                d_o.owngreetingPulser.reactivate()
            if d_o.ownwanderPulser.get_activity():
                d_o.ownwanderPulser.reactivate()
        else:
            pront(f'{d_o.art_d().capitalize()} is an inanimate object and does not respond.')
        inc_turn()

    def prioritize_d_o(self, d_o):
        priority = 0
        if isinstance(d_o, NPC):
            priority += 5
        return (d_o, priority)

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(d_o, NPC):
            if i_o.is_known():
                priority += 4
            else:
                priority -=8
            if i_o in d_o.get_tell_responses() or i_o in d_o.get_tell_event_triggers():
                priority += 3
            else:
                priority -= 6
        else:
            priority -= 1
        return (i_o, priority)

    def infer_nouns(self, alist):
        new = []
        num = alist[0][1]
        for x in alist:
            if x[1] == num:
                new.append(x[0])
            elif x[1] > num:
                num = x[1]
                new = [x[0]]
        if len(new) > 1 and num <= 0:
            return [new[0]]
        return new
tell = Tell('tell_about', ['tell', 'inform', 'enlighten', 'notify'], ('about',))
tell.set_d_o_requires_contact(False)
tell.set_i_o_requires_contact(False)
tell.set_i_o_requires_sight(False)

class Show(Verb2):
    def body(self, d_o, i_o):
        if isinstance(i_o, NPC):
            if d_o in i_o.get_show_responses():
                q = i_o.get_show_responses()[d_o]
                r = q[0]
                if q[1]:
                    r = '"' + r + '"'
                pront(r)
                for x in q[2]:
                    x.make_known()
            elif d_o in i_o.get_show_event_triggers():
                i_o.do_show_event(d_o)
            else:
                pront(f'"{i_o.get_unknown_show_msg()}"')
            if i_o.owngreetingPulser.get_activity():
                i_o.owngreetingPulser.reactivate()
            if i_o.ownwanderPulser.get_activity():
                i_o.ownwanderPulser.reactivate()
        else:
            pront(f'{i_o.art_d().capitalize()} is an inanimate object and does not respond.')
        inc_turn()

    def prioritize_i_o(self, d_o, i_o):
        priority = 0
        if isinstance(i_o, NPC):
            if d_o in i_o.get_show_responses() or d_o in i_o.get_show_event_triggers():
                priority += 3
            else:
                priority -= 6
        else:
            priority -= 1
        return (i_o, priority)
show = Show('show_to', ['show', 'reveal', 'display', 'point out', 'indicate'], ('to',))
show.set_d_o_requires_contact(False)
show.set_i_o_requires_contact(False)

class Say(VerbLit):
    def body(self, d_o):
        if d_o in ['bean', 'beans', 'borgar', 'shak', 'frie', 'hecc', 'meem', 'meme', 'it is wednesday, my dudes', 'duck', 'ducc', 'all birds are ducks', 'plugh', 'xyzzy', 'count leaves', 'kek', 'fr*ck', 'h*ck', 'finsh', 'fonsh', 'sheej', 'sheej tits', 'i hate sand', 'thicc', 'chungus', 'big chungus', 'waluigi', 'luigi', 'did you ever hear the tradgedy of darth plagueis the wise?', 'arma virumque cano', 'arma vivmqve cano', 'beef', 'beeves', 'b', 'leopards ate my face', 'embiggen', 'imbibe', 'succ', 'whomst', 'hewwo', '42', '69', '420', 'heck']:
            pront('You say "' + d_o + '." A hollow voice says, "Fool!"')
        elif d_o == 'it is wednesday my dudes':
            pront('You say "' + d_o + '." An indignant voice says, "You forgot a comma!"')
        else:
            pront('You say "' + d_o + '." Nothing happens.')
        inc_turn()
say = Say('say', ['say', 'announce', 'state', 'declare', 'incant'])

class Write(VerbLit2):
    def body(self, d_o, i_o):
        pront(f'You do not have a pen.')
write = Write('write_on', ['write', 'scrawl', 'scribble', 'jot down'], ('in', 'on'))

class Set(Verb2Lit):
    def body(self, d_o, i_o):
        pront(f'{d_o.art_d().capitalize()} is not something that can be set to anything.')
set = Set('set_to', ['set', 'turn', 'rotate', 'twist'], ('to', 'at', 'towards'))
#Space for remaps
