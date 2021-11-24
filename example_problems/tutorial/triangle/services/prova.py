import triangle_lib as tl


bt = [["A"],["B","C"],["D","D","F"],["E","H","A","B"]] #,["F","F","F","P","L"],["A","G","M","N","A","A"]]
st = [["D"],["H","A"]]

small = []
small_elements = len(st)
big= []
big_elements = len(bt)
for s in st:
    small += s
for b in bt:
    big += b

livello = 1
wait_count = 0
count = 1
match = 0
line = 0
for i in range(len(big)):
    if i >= livello*(livello+1)/2:
        livello +=1
    for j in range(len(st[line])):
        print([i,j])
        if big[i+j] == small[match]:
            match+=1
            print("match")
            
     
    
        
                
                
                
            
        
     
        
        
            
    
