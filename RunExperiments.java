/*
CSE6140 HW1
This is an example of how your experiments should look like.
Feel free to use and modify the code below, or write your own experimental code, as long as it produces the desired output.
*/
package YuzhouLiA1P4;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;

public class RunExperiments{
	public static void main(String[] args) throws IOException{


		if (args.length < 3) {
			System.err.println("Unexpected number of command line arguments");
			System.exit(1);
		}

		String graph_file = args[0];
		String change_file = args[1];
		String output_file = args[2];

		PrintWriter output;
		output = new PrintWriter(output_file, "UTF-8");

		Graph G = parseEdges(graph_file);
		Graph stdgraph = new Graph(G.size());
		Tree treeToBeComputed = new Tree(G.size());
		Tree newstdmst = new Tree(stdgraph.size());
		long startMST = System.nanoTime();
		int MSTweight = G.computeMST(treeToBeComputed,stdgraph);
		long finishMST = System.nanoTime();

		//Subtract the start time from the finish time to get the actual algorithm running time
		double MSTtotal = (finishMST - startMST)/1000000.0;

		//Write to output file the initial MST weight and time
		output.println(Integer.toString(MSTweight) + " " + Double.toString(MSTtotal));

		//Iterate through changes file
		BufferedReader br = new BufferedReader(new FileReader(change_file));
		String line = br.readLine();
		String[] split = line.split(" ");
		//int num_changes = Integer.parseInt(split[0]);
		int u, v, weight;

		while ((line = br.readLine()) != null) {
			split = line.split(" ");
			u = Integer.parseInt(split[0]);
			v = Integer.parseInt(split[1]);
			weight = Integer.parseInt(split[2]);

			//Run your recomputeMST function to recalculate the new weight of the MST given the addition of this new edge
			//Note: you are responsible for maintaining the MST in order to update the cost without recalculating the entire MST
			long start_newMST = System.nanoTime();
			int newMST_weight = stdgraph.recomputeMST(u,v,weight,newstdmst);
			long finish_newMST = System.nanoTime();

			double newMST_total = (finish_newMST - start_newMST)/1000000.0;

			//Write new MST weight and time to output file
			output.println(Integer.toString(newMST_weight) + " " + Double.toString(newMST_total));


		}

		output.close();
		br.close();




	}

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
}