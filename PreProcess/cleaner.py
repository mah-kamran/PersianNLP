
from __future__ import print_function
import codecs
import regex
import unicodedata

with codecs.open( 'Sources\lexicon.txt' , encoding='utf8')as f:
        lexicon = regex.split(r'\s+', regex.sub(r'[,\-!?.]', ' ', f.read()).strip())
        
with codecs.open( 'Sources\past-verb-stems.txt' , encoding='utf8')as f:
        past_verb_stem = regex.split(r'\s+', regex.sub(r'[,\-!?.]', ' ', f.read()).strip())
        
with codecs.open( 'Sources\present-verb-stems.txt' , encoding='utf8')as f:
        presnet_verb_stem = regex.split(r'\s+', regex.sub(r'[,\-!?.]', ' ', f.read()).strip())
               
with codecs.open( 'Sources\sec_suffix.txt' , encoding='utf8')as f:
        sec_suffix = regex.split(r'\s+', regex.sub(r'[,\-!?.]', ' ', f.read()).strip())

with codecs.open( 'Sources\prefix.txt' , encoding='utf8')as f:
        prefix = regex.split(r'\s+', regex.sub(r'[,\-!?.]', ' ', f.read()).strip())
        
with codecs.open( 'Sources\Exceptions.txt' , encoding='utf8')as f:
        Exceptions = regex.split(r'\s+', regex.sub(r'[,\-!?.]', ' ', f.read()).strip())
        
with codecs.open(  'Sources\suffix.txt' , encoding='utf8')as f:
        noun_maker_suffix = regex.split(r'\s+', regex.sub(r'[,\-!?.]', ' ', f.read()).strip())

        
###############################################~~~~~~~define input file~~~~~~~~##########################
with codecs.open( 'Inputs\sample-lda.csv' , encoding='utf8')as f:
        text =  f.read().strip()  
        
#########################################################################################################
      
table_persian_to_english = {
         1776: 48,  # 0 
         1777: 49,  # 1
         1778: 50,  # 2
         1779: 51,  # 3
         1780: 52,  # 4
         1781: 53,  # 
         1782: 54,  # 6
         1783: 55,  # 7
         1784: 56,  # 8
         1785: 57,  # 9
         1563: 59,  # ;
         1548: 44,  #,
         1567: 63  #?
         }  

table_english_to_persian = {
         48: 1776,  # 0 
         49: 1777,  # 1
         50: 1778,  # 2
         51: 1779,  # 3
         52: 1780,  # 4
         53: 1781,  # 5
         54: 1782,  # 6
         55: 1783,  # 7
         56: 1784,  # 8
         57: 1785,  # 9
         59: 1563,  #;
         44: 1548,  #,
         63: 1567   #?
         }  
arabi_h='ة'  
persian_h='ه'
yah_hamza='ئ'
persian_yah='ی'
arabic_yah='ي'
persian_kaf='ک'
arabic_kaf='ك'
alef_mad='آ'
alef_mad_diff='آ'
Arabic_Persian_Charachters = {        
            yah_hamza:persian_yah,
            arabic_yah:persian_yah,
            arabic_kaf:persian_kaf,
            alef_mad_diff:alef_mad,
            arabi_h :persian_h           
          }

naghli_baeed_suff='(ه بود|ه ای|ه باش|ه است|ه ام)?'
simple_suff='(?P<suff>(م|ی|د|یم|ید|ند|مان)?)'
khah='(خواهم|خواهی|خواهد|خواهیم|خواهید|خواهند)'
mi='(می|می\s|می\u200c|نمی|نمی\s|نمی\u200c)'  
persian_rang='[\u06A9\u06AF\u06C0\u06CC\u060C\u062A\u062B\u062C\u062D\u062E\u062F\u063A\u064A\u064B\u064C\u064D\u064E\u0621-\u0629\u0630-\u0639\u0641-\u0654]'

###########initial parameters ##########
split_english_persian=True
remove_redundant_chars=False
numbers_context=True
sapce_chars_alphabet=True
remove_tanvins=True

def space_to_halfspace_prefix(core , matched):
#    print( 'space_to_halfspace_prefix :' + ' core =' + core + 'matched= ' + str(matched) )
    space_at_start=False
    space_at_end=False
    return_string=matched
    if(matched.endswith(' ')):         
        space_at_end=True 
#        print(space_at_end)
    if(matched.startswith(' ')): 
        space_at_start=True     
    if(lexicon.count(core)>0 ):
        return_string=regex.sub('\s', '\u200c', matched.strip())
        if(space_at_start):
            return_string=' '+return_string
        if(space_at_end):
            return_string=return_string+' ' 
#    print ('return_string='+return_string)                
    return return_string

def space_to_halfspace_suffix(core  , matched):
#    print( 'space_to_halfspace_suffix :' + ' core =' + core + 'matched= ' + str(matched) )
    space_at_start=matched.startswith(' ')
    space_at_end=matched.endswith(' ')
    return_string=matched
    if(lexicon.count(core)>0 ):
        return_string=regex.sub('\s', '\u200c', matched)
        if(space_at_start):            
            return_string=' '+return_string
        if(space_at_end):
            return_string=return_string+' '     
#    print('return_string=' + return_string)
    return return_string     

def space_remover_noun_maker_suff(core , matched):  
#    print('space_remover_noun_maker_suff :' + ' core =' + core + 'matched= ' + matched)    
    if(lexicon.count(regex.sub('\s', '', matched.strip()))>0):    
#        print( 'space_remover_noun_maker_suff_returnValue'+ regex.sub('\s', '', matched.strip()))
        return regex.sub('\s', '', matched.strip())
    return matched    

def past_future_verb(mi_pre, khah_per, stem , matched):
#    print('past_future_verb :'+' mi_pre_future='+ mi_pre,'khah_per='+khah_per,'stem='+stem ,'matched='+matched)
    matched=regex.sub(mi_pre, mi_pre.strip()+'\u200c' ,matched)
    matched=regex.sub(khah_per, khah_per.strip()+'\u200c' ,matched)
    matched=regex.sub('\s' , '\u200c'  ,  matched)
    return matched


def present_verb(mi_pre, stem ,suff, matched ):
#    print('present_verb : '+ 'mi_pre= ' + mi_pre + ' , stem =' + stem + ' suff=' + suff + ', matched =' +matched)
    if(Exceptions.count(matched)>0):
        return(matched)    
    if( (presnet_verb_stem.count(stem) >0)): 
		 #todo : identified verbs can be labeled 
        return (mi_pre.strip() + '\u200c' + stem  +suff)    
    return matched

def match_redundant_lexicon(match):
#    print('match_redundant_lexicon : matched word= ' + match)
    temp=regex.sub(r'(\D+?)\1+', r'\1' , match)
    if (lexicon.count(match.strip())>0):          
        return match
    if(lexicon.count(temp.strip())>0):        
        return temp
    return match

def sec_suffix_debug(core , suffix  , matched):
    if(lexicon.count(matched)>0):        
        return matched
    return core+'\u200c'+suffix

def sapce_chars_alphabet (first ,second , third , matched):
#    print('sapce_chars_alphabet : first= '+ str(first) + ', second=' +str(second)+', third='+ str(third) )
    return (first + ' ' + second + ' ' +  third)

def CleanText(inputText):

	###############################################~~~~~~~start~~~~~~~~#############################################
	clean_text=unicodedata.normalize('NFKD', text)
	pattern = "|".join(map(regex.escape, Arabic_Persian_Charachters.keys()))
	clean_text=regex.sub(pattern, lambda m: Arabic_Persian_Charachters[m.group()], clean_text)

	################################################################### remove tanvins #############################################################
	#u0654=hamze ,#u0651=tashdid', #u0650=kasre,#u064f =zamme ,#u064b = tanvin e fathe ,#u64D=tanvin e kasre ,#u64c=tanvin e zamme ,#u064e = fathe
	if(remove_tanvins):
        clean_text=regex.sub('[\u0654\u0651\u0650\u064B\u064F\u064C\u064D\u0652\u064C]' , '' , clean_text)
	################################################################################################################################################

####################################################### remove tanvins #############################################################################				###############################################################################
	if(sapce_chars_alphabet):     
    #edit spaces in special chars 
		clean_text=regex.sub(r'(?P<first>[a-zA-Z]?)(?P<second>[(\){\}[\]\'"!<>:.;,،؛؟\?_-]|(?p)(\d+))(?P<third>[a-zA-Z]?)' , lambda m: sapce_chars_alphabet(m.group('first'),m.group('second'),m.group('third'),m.group(0)), clean_text)
###################################################################################################################################################################################################################################

######################### remove_redundant_chars ######################################################################
	if(remove_redundant_chars):	
    clean_text=regex.sub('\s\u200c' , '\s' , clean_text )
    #remove keshide form 
    clean_text=regex.sub(r'[ـ\r]', ''  , clean_text)
    #remove extra spaces 
    clean_text=regex.sub(r'([\s\n\r\u200ck])\1+' , r'\1'  , clean_text)
    #more than 2 occurrence  is reduce to 2 
    fixed_text=regex.sub(r'(\D)\1+', r'\1'r'\1', clean_text)
    #remove redundant chars according to lexicon
    clean_text = regex.sub(r'\w*(.+?)\1+\w*(\s|\u200c)', lambda m: match_redundant_lexicon(m.group(0)), fixed_text)    
#######################################################################################################################

################################## translate numbers according to their context #############################################################
	if(numbers_context):
    clean_text=regex.sub('([a-zA-Z])([^a-zA-Zء-ی]+)([a-zA-Z]+\s*?)' , lambda m: m.group(0).translate(table_persian_to_english) , clean_text)
    clean_text=regex.sub('([ء-ی]+)([^a-zA-Zء-ی]+)([ء-ی])'  , lambda m: m.group(0).translate(table_english_to_persian) , clean_text)    
#############################################################################################################################################

###########################################split English words  sticked to Persian words#################
	if(split_english_persian):
     clean_text=regex.sub(r'('+persian_rang+'+)([a-zA-Z]+)('+persian_rang+'+)', r'\1 \2 \3' , clean_text)
     clean_text=regex.sub(r'([a-zA-Z]+)('+persian_rang+'+)([a-zA-Z]+)', r'\1 \2 \3' , clean_text)
#########################################################################################################

####################################################################  present verb normalization  #############################################################################################
	clean_text=regex.sub('(?p)(?<=(\s|\u200c))(?P<mi>(ن?(می|می\s)))' +  '(?P<stem>'+'|'.join(presnet_verb_stem)+')' + simple_suff + '(?=\s)' , lambda m: present_verb(m.group('mi') , m.group('stem') , m.group('suff') ,m.group(0)) , clean_text)
##############################################################################################################################################################################################

#################################################################################################################### past and future verb normalization  ####################################################################################################################
	clean_text=regex.sub('(?p)(?P<mi>'+ mi + ')?(?P<khah>' + khah + '(\s|\u200c)?)?' +'ن?'+'(?P<stem>'+'|'.join(past_verb_stem)+')+' + simple_suff  + naghli_baeed_suff ,lambda m: past_future_verb(str(m.group('mi')),str(m.group('khah')),str(m.group('stem')),str(m.group(0))) , clean_text )
####################################################################################################################################################################################################################################################################################

############################################################################# normal spaces in  noun prefixes ##################################################################################################################

#clean_text = regex.sub('(?!V_)(?<=(\s|\u200c))(('+'|'.join(prefix)+')'+'\s?'+'(?P<core>'+persian_rang+'{2,})' +'\s?('+'|'.join(noun_maker_suffix)+')?(?=(\s|\u200c))?)+' , lambda m: space_to_halfspace_prefix(m.group('core') , m.group(0) ), clean_text)

	clean_text = regex.sub('(\s|\u200c)('+'|'.join(prefix)+')'+'\s?'+'(?P<core>'+persian_rang+'{2,})' +'\s?('+'|'.join(noun_maker_suffix)+')?((\s|\u200c))+' , lambda m: space_to_halfspace_prefix(m.group('core') , m.group(0) ), clean_text)
##############################################################################################################################################################################################################################

######################################################################################### remove noun suffix spaces #########################################################################################################################################
	clean_text = regex.sub('(?<=(\s|\u200c))(?P<core>'+persian_rang+'{2,})'+'\s('+'|'.join(noun_maker_suffix)+')(?=(\s|\u200c))' , lambda m: space_remover_noun_maker_suff(m.group('core') , m.group(0)), clean_text)

	clean_text = regex.sub( r'(?<=(\s|\u200c))'+'(?P<core>'+'('+'|'.join(lexicon)+'))' +'\s?'+ '(?p)(?P<suffix>('+'|'.join(sec_suffix)+'))+' + '(?=(\s|\u200c))'  ,  lambda m: sec_suffix_debug(m.group('core') ,m.group('suffix'), m.group(0)) , clean_text)
#############################################################################################################################################################################################################################################################

######################################## normal space for ی ###########################################
	clean_text=regex.sub(r'('+persian_rang+'{2,}ه)(\s)(ی)(?=(\s|\u200c))' ,  r'\1\u200c\3' , clean_text)
########################################################################################################

	print('done')
	print(clean_text)

###############################################~~~~~~~define input file~~~~~~~~##########################
	file = codecs.open("normalized.txt", "w", "utf-8")
	file.write(clean_text)
	file.close()
	return (clean_text)
##########################################################################################################
