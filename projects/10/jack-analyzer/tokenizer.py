import os

jack_keyword = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
jack_symbol = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]

class Tokenizer:
  def __init__(self, input_file):
    self.tokens = []
    self.current_token_index = 0
    self.current_token = None
    self.token_type = None
    with open(input_file) as f:
      self.content = self._remove_comments(f.read())
      self._skip_whitespace()

  def has_more_tokens(self):
    return self.current_token_index < len(self.content) - 1

  def advance(self):
    if self._read_current_index() in jack_symbol:
      self.token_type = "symbol"
      self.current_token = self._read_current_index()
      self.current_token_index += 1
      self._skip_whitespace()
      return
    
    if self._read_current_index() == '"':
      self.token_type = "stringConstant"
      self.current_token = self._read_token(lambda c: c != '"', include_wrappers=True)
      self._skip_whitespace()
      return
    
    if self._read_current_index().isdigit():
      self.token_type = "integerConstant"
      self.current_token = self._read_token(lambda c: c.isdigit())
      self._skip_whitespace()
      return
    
    if self._read_current_index().isalnum() or self._read_current_index() == "_":
      self.current_token = self._read_token(lambda c: c.isalnum() or c == "_")
      if self.current_token in jack_keyword:
        self.token_type = "keyword"
      else:
        self.token_type = "identifier"
      self._skip_whitespace()
      return

  def _read_token(self, condition, include_wrappers=False):
    if include_wrappers:
      self.current_token_index += 1
    start_index = self.current_token_index
    while condition(self._read_current_index()):
      self.current_token_index += 1
    token = self.content[start_index:self.current_token_index]
    if include_wrappers:
      self.current_token_index += 1
    return token

  def _read_current_index(self):
      if self.current_token_index >= len(self.content):
        return ''
      return self.content[self.current_token_index]

  def _skip_whitespace(self):
    while self._read_current_index() in [" ", "\n", "\t"]:
      self.current_token_index += 1
      
  def _remove_comments(self, content):
    result = []
    is_comment = False
    i = 0
    while i < len(content):
      if is_comment:
        if content[i] == "*" and content[i + 1] == "/":
          is_comment = False
          i += 1
      else:
        if content[i] == "/" and content[i + 1] == "/":
          while content[i] != "\n":
            i += 1
        elif content[i] == "/" and content[i + 1] == "*":
          is_comment = True
          i += 1
        else:
          result.append(content[i])
      i += 1
    return "".join(result)


if __name__ == "__main__":
  import sys
  
  if len(sys.argv) != 2:
    print("Usage: python tokenizer.py <input_file.jack>")
    sys.exit(1)

  input_files = []
  if os.path.isdir(sys.argv[1]):
    for file in os.listdir(sys.argv[1]):
      if file.endswith(".jack"):
        input_files.append(os.path.join(sys.argv[1], file))
  else:
    if sys.argv[1].endswith(".jack"):
      input_files.append(sys.argv[1])

  for input_file in input_files:
    tokenizer = Tokenizer(input_file)
    output_file = input_file.replace(".jack", "T.xml")
    with open(output_file, "w") as f:
      f.write("<tokens>\n")
      while tokenizer.has_more_tokens():
        tokenizer.advance()
        escaped_token = tokenizer.current_token
        if tokenizer.current_token == "<":
          escaped_token = "&lt;"
        elif tokenizer.current_token == ">":
          escaped_token = "&gt;"
        elif tokenizer.current_token == "&":
          escaped_token = "&amp;"
        f.write(f"<{tokenizer.token_type}> {escaped_token} </{tokenizer.token_type}>\n")
      f.write("</tokens>\n")
    print(f"Tokenized {input_file} to {output_file}")