import subprocess
import re


class Crontab:
    """
    Crontab class.
    Allow to create, remove, disable an enable a Linux crontab line
    """

    def __init__(self):
        self.hour = 0
        self.minute = 0
        self.period = "*"
        self.command = "echo test"
        self.comment = "piclodio"

    def create(self):
        """add line to the crontab"""
        # get actual crontab
        mycron = self.__getactualcrontab()
        # add the new line the the end
        line = str(self.minute)+" "+str(self.hour)+" * * "+str(self.period)+" "+str(self.command)+" #"+str(self.comment)
        mycron.append(line)
        # write it in a temp file
        f = open("/tmp/newcron.txt", "w")
        for line in mycron:
            f.write(line)
            f.write('\n')

        f.close()
        # write the crontab
        self.__writecrontab()

    def disable(self):
        """ disable from the crontab. Commeent the line into the crontab """
        # get actual crontab
        mycron = self.__getactualcrontab()

        # open temp file
        f = open("/tmp/newcron.txt", "w")

        # locate the line
        for line in mycron:
            if self.comment in line:
                if self.__isenable():
                    commentedline = "# "+line+"\n"
                    f.write(commentedline)
                else:  # allready disable, we do not touch anything
                    f.write(line)
            else:
                f.write(line+"\n")

        # close temp file
        f.close()
        # write the crontab
        self.__writecrontab()

    def enable(self):
        """ remove comment car ahead the line if present"""
        # get actual crontab
        mycron = self.__getactualcrontab()

        # open temp file
        f = open("/tmp/newcron.txt", "w")

        # locate the line
        for line in mycron:
            if self.comment in line:
                if not self.__isenable():  # check if not already enable
                    # extract line without comment
                    indexcomment = line.index('#')
                    linewithoutcomment = line[indexcomment+2:len(line)]
                    f.write(linewithoutcomment)
                else:  # already enable, write line without touch anything
                    f.write(line)

            else:
                f.write(line+"\n")

        # close temp file
        f.close()
        # write the crontab
        self.__writecrontab()

    def remove(self):
        """ Remove the line in the crontab by his comment """
        # get actual crontab
        mycron = self.__getactualcrontab()
        newcron = []

        # locate the line
        for line in mycron:
            if self.comment not in line:
                newcron.append(line)
                newcron.append('\n')

        # open temp file
        f = open("/tmp/newcron.txt", "w")
        for line in newcron:
            f.write(line)
        # close temp file
        f.close()
        # write the crontab
        self.__writecrontab()

    def __getactualcrontab(self):
        """ Return a dict of actual crontab """
        # get actual crontab
        p = subprocess.Popen("crontab -l", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        mycron = str(output)
        return mycron.split("\n")

    def __writecrontab(self):
        """ Write the temp file into the crontab  """
        # save the crontab from the temp file
        p = subprocess.Popen("crontab /tmp/newcron.txt", stdout=subprocess.PIPE, shell=True)
        p.communicate()

    def __isenable(self):
        """ return True id the cron job line is not commented  """
        # get actual crontab
        mycron = self.__getactualcrontab()

        # locate the line
        for line in mycron:
            if self.comment in line:
                regex = re.compile("^#")
                test = regex.match(line)
                if test:
                    # is disable
                    return False
                else:
                    # is enable
                    return True
        return False


