from Parser.Dictionaries import ReadyPartDict, EntitiesDict, GlueWordDict, PredicatesDict, CharactersDict, FindItem
from Parser.Flexies import FlexiesDict


class Parser(object):
    flexies = [FlexiesDict()]
    dicts = [ReadyPartDict(), EntitiesDict(flexies), CharactersDict(flexies), PredicatesDict(flexies)]
    gw = GlueWordDict()

    def mode_parse(self):
        self.mode = self.parse_input
        return "mode: parse"

    def mode_syn(self):
        self.mode = self.syn_from_input
        return "mode: syn"

    def print_help(self):
        return "Aviable commands : /help for help; \n/parse for change mode to parse; \n/syn for change mode to " \
               "syn.\nIn parse mode you need print any string for parsing it. \nIn syn (synthesis) mode you aviable " \
               "next templates: \nсуществительное СУ gender number case\nприлагательное ПП gender number " \
               "case\nглагол ГЛ gender number;\nчислительное ЧИ case\n" \
               "gender, numbers and case coding by two kirrilic letters."

    commands = {"/parse": mode_parse, "/syn": mode_syn, "/help": print_help}

    def __init__(self) -> None:
        self.mode = self.parse_input

    def input(self, str):
        if str is None or len(str) == 0:
            return "None"
        if str[0] == "/":
            command = self.commands.get(str)
            if command is not None:
                return command(self)
            else:
                return "command not found"
        else:
            return self.mode(str)

    def parse_input(self, input_str):
        input_str = input_str.strip().upper()
        input_str = self.gw.transform(input_str)
        words = input_str.split()
        phrases = []
        for word in words:
            phrases.append(self.parse_word(word))
        return '\n'.join(str(x) for x in phrases)

    def syn_from_input(self, input_str):
        input_str = input_str.strip().upper().split()
        part_speech = input_str[1]
        find_item = None
        if part_speech == 'СУ':
            find_item = FindItem(input_str[0], input_str[1], input_str[2], input_str[3], input_str[4])
        elif part_speech == 'ПП':
            find_item = FindItem(input_str[0], input_str[1], input_str[2], input_str[3], input_str[4])
        elif part_speech == 'ГЛ':
            find_item = FindItem(input_str[0], input_str[1], input_str[2], input_str[3], None)
        elif part_speech == 'ЧИ':
            find_item = FindItem(input_str[0], input_str[1], None, None, input_str[2])
        for one_dict in self.dicts:
            parse = one_dict.synthesis(find_item)
            if parse is not None:
                return parse
        return input_str[0] + "_НФ"

    def parse_word(self, word):
        for one_dict in self.dicts:
            parse = one_dict.find(word)
            if parse is not None:
                return word + " - " + parse.to_string()
        return word + " Неопределенная часть речи"
