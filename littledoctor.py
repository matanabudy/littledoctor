import sys
import csv
import shutil
import os

USAGE =                 'Usage: littledoctor.py [survivor_name] [start_value] [end_value] [step]'
FASM_PATH =             os.path.dirname(__file__)+'.\\fasm'
COREWARS_SCORES_PATH =  os.path.dirname(__file__)+'.\\special8086\\scores.csv'
# KYRIL_SCORES_PATH =     os.path.dirname(__file__)+'.\\even_better_kyril\\scores.csv'
OPTIM_SCORES_PATH =     os.path.dirname(__file__)+'.\\optim_scores.csv'
DOSBOX_PATH =           os.path.dirname(__file__)+'.\\DOSBoxPortable'
# KYRIL_PATH =            os.path.dirname(__file__)+'.\\kyril\\survivors'
COREWARS_PATH =         os.path.dirname(__file__)+'.\\special8086\\survivors'
max_score =             0
max_line =              ''
all_times_max =         0

def replace(file_path, pattern, subst):
    from tempfile import mkstemp
    from shutil import move
    from os import remove, close, system
    #Replace function from: https://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file_path)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


def read_scores(scores_path, survivor_name):
    reader = csv.reader(open(scores_path, "rb"), delimiter=':', quoting=csv.QUOTE_NONE)

    survivor_row=['Error', 0]
    
    split_list1=[]
    split_list2=[]

    for row in reader:
        split_list1.append(', '.join(row)) #seperates rows

    for column in split_list1:
        split_list2.append(column.split(',')) #seperates rows to [survivor, score]

    for score in split_list2:
        #searches for survivor result and saves it
        #score looks like: score[survivor, score]
        if score[0]==survivor_name:
            survivor_row=score
            break

    return survivor_row

def write_scores(OPTIM_SCORES_PATH, score_object, optimized_line):
    global max_score
    global max_line
    
    myfile=open(OPTIM_SCORES_PATH, 'wb')
    c=csv.writer(myfile)
    
    score_object.append(optimized_line)
    current_score=float(score_object[1])
    
    if int(current_score)>max_score:
        max_score=int(current_score)
        max_line=score_object[2]

    print 'Max score: %s' % (str(max_score))

    c.writerow([score_object[0], max_score, max_line])
    myfile.close()

def fasm_survivor(survivor_name):
    
    run_dosbox_cmd='DOSBoxPortable.exe'
    fasm_first_survivor='-c "fasm %s1.asm %s1"' %(survivor_name,survivor_name)
    fasm_second_survivor='-c "fasm %s2.asm %s2"' %(survivor_name,survivor_name)
    exit_dosbox_cmd='-c "exit"'
    
    os.chdir(DOSBOX_PATH)
    os.system(run_dosbox_cmd+" "+fasm_first_survivor+" "+fasm_second_survivor+" "+exit_dosbox_cmd)
    
def copy_survivor(survivor_name,path):
    
    src = FASM_PATH+"/%s1" % (survivor_name)
    dst =  path
    shutil.copy(src,dst)
    src = FASM_PATH+"/%s2" % (survivor_name)
    shutil.copy(src,dst)

def create_survivor(survivor_name,place):
    
    fasm_survivor(survivor_name)
    
    # if place == "kyril":
        # copy_survivor(survivor_name , KYRIL_PATH)
        
    if place == "corewars":
        copy_survivor(survivor_name , COREWARS_PATH)
        
    else:
        print USAGE
        print "Maybe spelling mistake?"

def run_game(game):
    
    # if game=="kyril":
        # os.chdir(os.path.dirname(__file__)+'.\\kyril')
        # os.system('nightly12_02_14.jar')
        
    if game=="corewars":
        os.chdir(os.path.dirname(__file__)+'.\\special8086')
        os.system('corewars.jar')

if  (len(sys.argv)<5):
    print USAGE
    sys.exit(0)
    
survivor_name = sys.argv[1].upper()

survivor1_path = FASM_PATH+'\\%s1.asm' % (survivor_name)
survivor2_path = FASM_PATH+'\\%s2.asm' % (survivor_name)

start_value = int(sys.argv[2], 16)
end_value = int(sys.argv[3], 16)

step = int(sys.argv[4])

print 'Welcome to The Doctor!\n'

pattern = raw_input('Enter pattern-->')

s=pattern

print '\nThe Doctor will now optimize %s, replacing %s between %s-%s' % (survivor_name, pattern, str(start_value), str(end_value))
print '-----'

print 'Starting to optimize...'

for x in range(start_value, end_value, step):
    rounds_left=(end_value-x)/step
    x = hex(x) #convert to a string represantation of hex like this: 0x3
    x = x[0]+x[2:] #deletes the "x" part

    line_to_optimize = s.split(' ')[0]+' %s' % (x)
    
    print '-----'

    print 'Optimizing with: %s' % (line_to_optimize)
    print '%s rounds are left' % (str(rounds_left))
    
    replace(survivor1_path, s, line_to_optimize)
    replace(survivor2_path, s, line_to_optimize)
    
    create_survivor(survivor_name,place)
    run_game(place)
    
    if place=='corewars':
        survivor_row=read_scores(COREWARS_SCORES_PATH, survivor_name)
    # elif place=='kyril':
        # survivor_row=read_scores(KYRIL_SCORES_PATH, survivor_name)

    print '%s scored %s in the this game\n' % (survivor_name, survivor_row[1])
    
    write_scores(OPTIM_SCORES_PATH, survivor_row, line_to_optimize)
    
    s = line_to_optimize

best_survivor = read_scores(OPTIM_SCORES_PATH,survivor_name)
line_to_replace = best_survivor[2]
print '\nThe winning line is: %s' % (line_to_replace)
print 'The winning score is: %s\n' % (best_survivor[1])

if (int(best_survivor[1])>all_times_max):
    print 'It is an all times record!'
    print '%s was updated' % (survivor_name)
    print '(IMPORTANT: Please update the all times record in the code)'

    replace(survivor1_path,s,line_to_replace)
    replace(survivor2_path,s,line_to_replace)
    
else:
    replace(survivor1_path,s,pattern)
    replace(survivor2_path,s,pattern)
    print 'But it is not an all times recrod...'
    print 'No update, but keep up the good work!'
