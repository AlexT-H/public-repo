

# parses through given file, adding weights to connecting chars
def preprocess(srcFilename, n):

    model_dict = {}
    with open(srcFilename) as file:
        text = file.read().rstrip('\n')

        for index, char in enumerate(text):

            # checks for a sufficient n-gram size
            if index != (len(text) - 1) and index + n <= len(text):
                nGram = char
                for k in range(1, n):
                    nGram += text[index + k]

            # makes an initial, blank directory
            if nGram not in model_dict:
                model_dict[nGram] = {}

            value_dict = model_dict[nGram]

            # connects the value with the next character
            if index + n < len(text):
                value = text[index + n]
                if value in value_dict:
                    value_dict[value] += 1
                else:
                    value_dict[value] = 1
            else:
                value_dict[''] = 1

            # set n-gram to value dictionary
            model_dict[nGram] = value_dict

        return model_dict


####
#    Further Processing (Grammatical and Contextualization)
####
