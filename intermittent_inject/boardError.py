class BoardError(Exception):
  def __init__(self, issue):
    self.issue = issue
    
  def __str__(self):
    return repr("There's an issue with the board: " + self.issue)
