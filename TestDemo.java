package YuzhouLiA1P4;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class TestDemo {
	public static Graph parseEdges(String graph_file) throws IOException {
		
		BufferedReader br = new BufferedReader(new FileReader(graph_file));
		
		
		String line = br.readLine();
		String[] split = line.split(" ");
		int size = Integer.parseInt(split[0]);
		Graph g = new Graph(size);
		while ((line = br.readLine()) != null) {
			split = line.split(" ");
			int node1 = Integer.parseInt(split[0]);
			int node2 = Integer.parseInt(split[1]);
			int weight = Integer.parseInt(split[2]);
			g.addEdge(node1,node2,weight);
			
		}
		br.close();
		return g;
	}			
	public static void main(String[] args) throws IOException {
		
		Graph ggg = TestDemo.parseEdges("src/rmat1517.gr");
		Graph stmstgraph = new Graph(ggg.size());
		Tree MST = new Tree(ggg.size());
		System.out.println(ggg.computeMST(MST,stmstgraph));
		Tree newmst = new Tree(stmstgraph.size());
		BufferedReader br = new BufferedReader(new FileReader("src/rmat1517.extra"));
		String line = br.readLine();
		String[] split = line.split(" ");
		//int num_changes = Integer.parseInt(split[0]);
		int u, v, weight;
		int newMST_weight=0;
		while ((line = br.readLine()) != null) {
			split = line.split(" ");
			u = Integer.parseInt(split[0]);
			v = Integer.parseInt(split[1]);
			weight = Integer.parseInt(split[2]);

			//Run your recomputeMST function to recalculate the new weight of the MST given the addition of this new edge
			//Note: you are responsible for maintaining the MST in order to update the cost without recalculating the entire MST
			long start_newMST = System.nanoTime();
			newMST_weight = stmstgraph.recomputeMST(u,v,weight,newmst);
			long finish_newMST = System.nanoTime();
			double newMST_total = (finish_newMST - start_newMST)/1000000;
		
			System.out.println(newMST_weight);
			System.out.println(newMST_total);
			
	}
		br.close();
		
}
}
