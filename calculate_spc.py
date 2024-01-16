
#a more up-to-date version of this code is available on Minerva 
import sys,pickle,networkit,scipy
from scipy import sparse
from scipy.sparse import csgraph
from scipy.sparse import linalg as splinalg
import numpy as np 
import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input','-i',help='Address for the input network file',type=str,required=True)
    parser.add_argument('--output','-o',help='Output address prefix.',type=str,default='spc')
    parser.add_argument('--count','-c',help='Number of components to calculate',type=int,default=25)
    parser.add_argument('--delimiter','-d',help='Delimiter charachter in the linklist file, using "s" for space and "t" for tab',type=str,default='s')
    args=parser.parse_args()
    # if args.load == 'NONE':
    #     removal_dict = defaultdict(list)
    #     with open(args.remove,'r')

    input_addr = args.input#sys.argv[1]
    output_addr = args.output#sys.argv[2]
    delimiter=' ' 
    if args.delimiter == 's':
        delimiter = ' '
    elif args.delimiter =='t':
        delimiter ='\t'
    else:
        delimiter = args.delimiter
    reader = networkit.graphio.EdgeListReader(delimiter,0, continuous=False,directed=False)
    print('loading the graph into memory')
    G = reader.read(input_addr)
    node_count = G.numberOfNodes()
    print('graph loaded, saving the node mapping for later')
    print(f'Number of nodes {node_count}')
    nodemap = reader.getNodeMap()
    
    #pickle.dump(reader.getNodeMap(),open(output_addr+'_nodemap.pkl','wb'))
    print('generating the adjacency matrix')
    adj = networkit.algebraic.adjacencyMatrix(G)
    
    del G
    '''print(f'saving the adjacency matrix with the type {type(adj)}')
    if type(adj) == scipy.sparse._csr.csr_matrix:
        sparse.save_npz(f"{output_addr}_csr.npz", adj)
    elif type(adj) == np.ndarray:
        np.save(output_addr+'_ndarray.npy',adj)'''
    print('transforming the adjacency matrix into a normalized laplacian matrix...')
    nlap = csgraph.laplacian(adj, normed=True)
    del adj
    '''print(f'saving the laplacian...{type(nlap)}')
    if type(nlap) == scipy.sparse._csr.csr_matrix:
        sparse.save_npz(f"{output_addr}_nlap.npz", nlap)
    elif type(nlap) == np.ndarray:
        np.save(output_addr+'_nlap_ndarray.npy',nlap)'''
    print('deconmopsing the laplacian:')
    # neigs = linalg.eigh(nlap.toarray())
    eigenvecs = splinalg.eigsh(nlap,k=args.count,which='SM')
    del nlap
    inv_nodemap = {v: k for k, v in nodemap.items()}
    
    # pickle.dump(eigenvecs,open(f'{output_addr}_eigens.pklnp'))
    with open(output_addr,'wt') as outputfile:
        outputfile.write('id ')
        outputfile.write(' '.join([f'SPC_{i+1}' for i in range(args.count)]))
        
        for index in range(node_count):
            outputfile.write(f'{inv_nodemap[index]} ')
            outputfile.write(' '.join([str(eigenvecs[1][index,i]) for i in range(args.count)]))
    
    # pandas functionality update: 
    # sp_dict = {'cid':[]}
    # for i in range(args.count):
    #     sp_dict[f'SPC_{i+1}'] = []
    # for key in inv_nodemap:
    #     sp_dict['cid'].append(inv_nodemap[key])
    
    #     for i in range(args.count):
    #         sp_dict[f'SPC_{i+1}'].append(eigenvecs[key,i])
    # tspdf = pd.DataFrame.from_dict(sp_dict)
    
if __name__ == '__main__':
    main()