import os,argparse,gzip,glob

def read_relateds(related_file_addr):
    relateds = set()
    with open(related_file_addr,'r') as related_file:
        for line in related_file:
            relateds.add(line.strip())
    return relateds

def write_file(links,output_addr,min_length=6.0):
    count = 0
    with open(output_addr,'w') as output_file:
        for id1 in links:
            for id2 in links[id1]:
                count += 1
                if links[id1][id2] >= min_length:
                    output_file.write(f'{id1}\t{id2}\t{links[id1][id2]}\n')
    print(f'Total connection count is {count}')

def make_links(ibd_addr_list,id1_col=1,id2_col=3,ibd_col=-2,haploid_mode=False,min_len=3.0,sep=' ',removals=set()):
    links = {}
    # match_files_addr_list = [os.path.join(input_pre,f) for f in os.listdir(input_pre) if os.path.isfile(os.path.join(input_pre, f)) and f.endswith(f'{input_suff}')]
    # for addr in match_files_addr_list:
    for addr in ibd_addr_list:
        with gzip.open(addr,'rt') as match_file:
            for line in match_file:
                data = line.strip().split(sep)
                link_length = float(data[ibd_col])
                if link_length < min_len:
                    continue
                if haploid_mode:
                    id1= data[id1_col]
                    id2 = data[id2_col]
                else:
                    id1 = data[id1_col][:-2]
                    id2 = data[id2_col][:-2]
                if id1 in removals or id2 in removals:
                    continue
                if id1 in links:
                    if id2 in links[id1]:
                        links[id1][id2] += link_length
                        continue
                    elif id2 not in links:
                        links[id1][id2] = link_length
                        continue
                if id2 in links:
                    if id1 in links[id2]:
                        links[id2][id1] += link_length

                    else:
                        links[id2][id1] = link_length
                else:
                    links[id1] = {}
                    links[id1][id2] = link_length
    return links
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output','-o',help='Address for the output network file',type=str,required=True)
    parser.add_argument('--ibd-file-address','-i',help='Address for IBD files. If there are separated by chromosome, replace the chromosome number with @ in the address',type=str,required=True,dest='ibd_addr')
    # parser.add_argument('--ibd-file-suffix','-s',help='Suffix for the IBD file addresses (optional)',type=str,default='.match',required=False,dest='ibd_suff')
    parser.add_argument('--id1-column',help='Zero-based column index for the first ID column',type=int,default=1,dest='id1_col')
    parser.add_argument('--id2-column',help='Zero-based column index for the second ID column',type=int,default=3,dest='id2_col')
    parser.add_argument('--ibd-column',help='Zero-based column index for the aggregate IBD informaiton',type=int,default=-2,dest='ibd_col')
    parser.add_argument('--haploid-mode',help='Set this flag if the haplotype codes have the own column and are not appended to the individuals IDs',action='store_true',dest='haploid_mode')
    parser.add_argument('--minimum-segment-length',help='minimum length of IBD segments to be considered for aggregation',type=float,default=3,dest='min_seg_len')
    parser.add_argument('--minimum-agg-length',help='minimum aggreagate length o IBD sharing to be considered as an edge',type=float,default=6.0,dest='min_agg_len')
    parser.add_argument('--sep',help='Separator. Leave t for tab and s for space',type=str,default='s')
    parser.add_argument('--removal-file',help='address for the file containing individuals to remove',type=str,default='',dest='removal_file_addr')
    # parser.add_argument('--cluster','-c',help='Address of the file that includes member IDs',type=str,required=True)
    
    # parser.add_argument('')

    args = parser.parse_args()
    sep = args.sep
    if sep == 's':
        sep=' '
    if sep =='t':
        sep = '\t'
    if args.removal_file_addr == '':
        removals = set()
    else:
        removals = read_relateds(args.removal_file_addr)
    ibd_addr_list = None
    if '@' in args.ibd_addr:
        addr_pattern = args.ibd_addr.replace('@','*')
        ibd_addr_list = glob.glob(addr_pattern)
    else:
        ibd_addr_list = [args.ibd_addr]
    links = make_links(ibd_addr_list,
                       id1_col=args.id1_col,id2_col=args.id2_col,
                       ibd_col=args.ibd_col,haploid_mode=args.haploid_mode,
                       min_len=args.min_seg_len,sep=sep,removals=removals)
    write_file(links,args.output,args.min_agg_len)


if __name__ == '__main__':
    main()


