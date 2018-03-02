package webcrawler;

import java.util.*;
import java.io.*;

public class paths
{
    String workingDir;
    ArrayList<String> base;
    String[][] str;
    int p;
    
    public paths() {
        this.workingDir = "/home/devashish/Topology_Devashish";
        this.base = new ArrayList<String>();
        this.str = new String[1000][1000];
    }
    
    public void baseas(final String prefix, final String fprefix) {
        this.base.clear();
        try {
            final BufferedReader br = new BufferedReader(new FileReader(new File("/home/devashish/Topology_Devashish/SortFile_march.txt")));
            String[] splitted = null;
            int k = 1;
            System.out.println("CALCULATING BASE ASes : " + prefix);
            String strline;
            while ((strline = br.readLine()) != null) {
                splitted = strline.split(" ");
                k = 1;
                if (splitted[0].equals(prefix)) {
                    while (k < splitted.length) {
                        if (!this.base.contains(splitted[k])) {
                            this.base.add(splitted[k]);
                        }
                        ++k;
                    }
                }
            }
            br.close();
            System.out.println("PRINTING BASE ASes");
            for (final String s : this.base) {
                System.out.println(s);
            }
            System.out.println("NUMBER OF BASE ASes(COUNT) : ");
            System.out.println(this.base.size());
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public void frequencycallingfunction(final String prefix, final String fprefix) {
        System.out.println("FREQUENCY CALLING FUNCITION : " + prefix);
        try {
            for (final String s : this.base) {
                final String fileaddress = String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + s + ".txt";
                this.deleteblanklines(fileaddress);
            }
            for (final String s : this.base) {
                final String fileaddress = String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + s + ".txt";
                this.p = 0;
                for (int m = 0; m < 1000; ++m) {
                    for (int n = 0; n < 1000; ++n) {
                        this.str[m][n] = "a";
                    }
                }
                final BufferedReader textbr = new BufferedReader(new FileReader(new File(fileaddress)));
                final ArrayList<String> textrev = new ArrayList<String>();
                String[] textsplitted = null;
                String textline;
                while ((textline = textbr.readLine()) != null) {
                    textrev.clear();
                    textsplitted = textline.split(" ");
                    for (int i = textsplitted.length - 1; i > 2; --i) {
                        textrev.add(textsplitted[i]);
                    }
                    this.freq(textrev, fileaddress, s, prefix);
                    ++this.p;
                }
                textbr.close();
                final File file = new File(fileaddress);
                if (file.delete()) {
                    System.out.println(String.valueOf(file.getName()) + " is deleted!");
                }
                else {
                    System.out.println("Delete operation is failed.");
                }
                final File file2 = new File(fileaddress);
                if (!file2.exists()) {
                    file2.createNewFile();
                }
                final FileWriter fw = new FileWriter(file2.getAbsoluteFile(), true);
                final BufferedWriter bw3 = new BufferedWriter(fw);
                for (int c = 0; c < this.p; ++c) {
                    for (int d = 0; d < 1000; ++d) {
                        if (!this.str[c][d].equals("a")) {
                            bw3.write(this.str[c][d]);
                            bw3.write(" ");
                        }
                    }
                    bw3.newLine();
                }
                bw3.close();
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public void freq(final ArrayList<String> textpath, final String fileaddr, final String baseas, final String prefix) {
        int count = 0;
        try {
            final BufferedReader br = new BufferedReader(new FileReader(new File(String.valueOf(this.workingDir) + "/SortFile_march.txt")));
            final ArrayList<String> dumppath = new ArrayList<String>();
            String[] splitted = null;
            String strline;
            while ((strline = br.readLine()) != null) {
                dumppath.clear();
                splitted = strline.split(" ");
                if (splitted[0].equals(prefix)) {
                    for (int i = 1; i < splitted.length; ++i) {
                        dumppath.add(splitted[i]);
                    }
                }
                if (dumppath.contains(textpath) || dumppath.containsAll(textpath) || dumppath.equals(textpath)) {
                    ++count;
                }
            }
            Collections.reverse(textpath);
            int u = 3;
            this.str[this.p][0] = Integer.toString(0);
            this.str[this.p][1] = Integer.toString(0);
            this.str[this.p][2] = Integer.toString(count);
            for (final String k : textpath) {
                this.str[this.p][u++] = k;
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public void peers() {
        final String fileaddress = "C:/Users/rahul singh/workspace/webcrawler/peers/";
        final ArrayList<String> peer = new ArrayList<String>();
        String[] splitted = null;
        try {
            for (final String s : this.base) {
                final String fileaddr = String.valueOf(fileaddress.substring(0, fileaddress.length())) + "AS" + s + ".txt";
                final File file = new File(fileaddr);
                if (!file.exists()) {
                    file.createNewFile();
                }
                final FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
                final BufferedWriter bw = new BufferedWriter(fw);
                final BufferedReader br2 = new BufferedReader(new FileReader(new File("dumptrials.txt")));
                String strline;
                while ((strline = br2.readLine()) != null) {
                    splitted = strline.split(" ");
                    for (int i = 1; i < splitted.length; ++i) {
                        if (splitted[i].equals(s) && (i != splitted.length - 1 || i != 1)) {
                            if (i == splitted.length - 1) {
                                if (!peer.contains(splitted[i - 1])) {
                                    peer.add(splitted[i - 1]);
                                }
                            }
                            else if (i == 1) {
                                if (!peer.contains(splitted[i + 1])) {
                                    peer.add(splitted[i + 1]);
                                }
                            }
                            else {
                                if (!peer.contains(splitted[i - 1])) {
                                    peer.add(splitted[i - 1]);
                                }
                                if (!peer.contains(splitted[i + 1])) {
                                    peer.add(splitted[i + 1]);
                                }
                            }
                        }
                    }
                }
                br2.close();
                for (final String s2 : peer) {
                    if (!s2.equals(s)) {
                        bw.write(s2);
                        bw.newLine();
                    }
                }
                bw.close();
                peer.clear();
            }
            final String addr = "C:/Users/rahul singh/workspace/webcrawler/peers/";
            for (final String s3 : this.base) {
                final String faddr = String.valueOf(addr) + "AS" + s3 + ".txt";
                this.deleteblanklines(faddr);
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public void path(final String prefix, final String fprefix) {
        System.out.println("PATH FUNCTION : " + prefix);
        final boolean dir = new File(String.valueOf(this.workingDir) + "/paths/" + fprefix).mkdir();
        System.out.println("CREATING FOLDER FOR THIS PATH SET : " + dir);
        final String fileaddress = String.valueOf(this.workingDir) + "/paths/" + fprefix + "/";
        final ArrayList<String> aspath = new ArrayList<String>();
        aspath.clear();
        int k = 1;
        String[] splitted = null;
        try {
            final BufferedReader br = new BufferedReader(new FileReader(new File(String.valueOf(this.workingDir) + "/SortFile_march.txt")));
            String strline;
            while ((strline = br.readLine()) != null) {
                k = 1;
                splitted = strline.split(" ");
                if (splitted[0].equals(prefix)) {
                    for (int i = splitted.length - 1; i > 0; --i) {
                        final String fileaddr = String.valueOf(fileaddress.substring(0, fileaddress.length())) + splitted[i] + ".txt";
                        final File file = new File(fileaddr);
                        if (!file.exists()) {
                            file.createNewFile();
                        }
                        final FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
                        final BufferedWriter bw = new BufferedWriter(fw);
                        aspath.add("0");
                        aspath.add("0");
                        aspath.add("0");
                        for (int j = splitted.length - 1; j >= i; --j) {
                            aspath.add(splitted[j]);
                        }
                        final int r = pathequal(fileaddr, aspath);
                        if (r == 0) {
                            for (final String s : aspath) {
                                bw.write(s);
                                bw.write(" ");
                            }
                        }
                        bw.newLine();
                        bw.close();
                        aspath.clear();
                    }
                }
            }
            br.close();
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public static int pathequal(final String aspathfile, final ArrayList aspath) {
        try {
            final BufferedReader br = new BufferedReader(new FileReader(new File(aspathfile)));
            String[] splitted = null;
            int k = 0;
            String strline;
            while ((strline = br.readLine()) != null) {
                k = 0;
                splitted = strline.split(" ");
                if (splitted.length == aspath.size()) {
                    for (int i = 0; i < splitted.length && splitted[i].equals(aspath.get(i)); ++i) {
                        ++k;
                    }
                }
                if (k == aspath.size() && k == splitted.length) {
                    br.close();
                    return 1;
                }
            }
            br.close();
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
        return 0;
    }
    
    public void pathlengthcallingfunction(final String prefix, final String fprefix) {
        System.out.println("PATH LENGTH CALLING FUNCTION : " + prefix);
        final String fileaddress = String.valueOf(this.workingDir) + "/paths/" + fprefix + "/";
        for (final String s : this.base) {
            final String fileaddr = String.valueOf(fileaddress) + s + ".txt";
            this.deleteblanklines(fileaddr);
            this.pathlength(fileaddr);
            this.deleteblanklines(fileaddr);
        }
    }
    
    public void deleteblanklines(final String fileaddr) {
        try {
            final File inFile = new File(fileaddr);
            if (!inFile.isFile()) {
                System.out.println("Parameter is not an existing file");
                return;
            }
            final File tempFile = new File(String.valueOf(inFile.getAbsolutePath()) + ".tmp");
            final BufferedReader br = new BufferedReader(new FileReader(fileaddr));
            final PrintWriter pw = new PrintWriter(new FileWriter(tempFile));
            String line = null;
            while ((line = br.readLine()) != null) {
                if (!line.isEmpty()) {
                    pw.println(line);
                    pw.flush();
                }
            }
            pw.close();
            br.close();
            if (!inFile.delete()) {
                System.out.println("Could not delete file");
                return;
            }
            if (!tempFile.renameTo(inFile)) {
                System.out.println("Could not rename file");
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public void pathlength(final String fileaddr) {
        try {
            final BufferedReader br = new BufferedReader(new FileReader(new File(fileaddr)));
            String[] splitted = null;
            final String[][] str = new String[300][300];
            int p = 0;
            int q = 0;
            for (int i = 0; i < 300; ++i) {
                for (int j = 0; j < 300; ++j) {
                    str[i][j] = "a";
                }
            }
            String line;
            while ((line = br.readLine()) != null) {
                splitted = line.split(" ");
                for (int i = 0; i < splitted.length; ++i) {
                    str[p][q++] = splitted[i];
                }
                ++p;
                q = 0;
            }
            br.close();
            int count = 0;
            for (int i = 0; i < p; ++i) {
                for (int j = 0; j < 300; ++j) {
                    if (!str[i][j].equals("a")) {
                        ++count;
                    }
                }
                count -= 3;
                str[i][0] = Integer.toString(count);
                count = 0;
            }
            final File rfile = new File(fileaddr);
            if (rfile.delete()) {
                System.out.println(String.valueOf(rfile.getName()) + " is deleted!");
            }
            else {
                System.out.println("Delete operation is failed.");
            }
            final File file = new File(fileaddr);
            if (!file.exists()) {
                file.createNewFile();
            }
            final FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
            final BufferedWriter bw = new BufferedWriter(fw);
            for (int i = 0; i < p; ++i) {
                for (int j = 0; j < 300; ++j) {
                    if (!str[i][j].equals("a")) {
                        bw.write(str[i][j]);
                        bw.write(" ");
                    }
                }
                bw.newLine();
            }
            bw.close();
            fw.close();
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public void sortfilecallingfunction(final String prefix, final String fprefix) {
        System.out.println("SORT FILE CALLING FUNCTION : " + prefix);
        for (final String s : this.base) {
            final String fileaddress = String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + s + ".txt";
            this.sortfile(fileaddress);
        }
    }
    
    public void sortfile(final String fileaddr) {
        final String[][] str = new String[1000][1000];
        final String[] temp = new String[1000];
        for (int i = 0; i < 1000; ++i) {
            for (int j = 0; j < 1000; ++j) {
                str[i][j] = "a";
            }
        }
        for (int i = 0; i < 1000; ++i) {
            temp[i] = "a";
        }
        int p = 0;
        int q = 0;
        int k = 0;
        try {
            final BufferedReader br = new BufferedReader(new FileReader(new File(fileaddr)));
            String[] splitted = null;
            String strline;
            while ((strline = br.readLine()) != null) {
                splitted = strline.split(" ");
                for (int i = 0; i < splitted.length; ++i) {
                    str[p][q++] = splitted[i];
                }
                ++p;
                q = 0;
            }
            br.close();
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
        for (int i = 0; i < p - 1; ++i) {
            for (int j = i + 1; j < p; ++j) {
                if (Integer.parseInt(str[i][0]) > Integer.parseInt(str[j][0])) {
                    for (k = 0; k < 1000; ++k) {
                        temp[k] = str[i][k];
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[i][k] = "a";
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[i][k] = str[j][k];
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[j][k] = "a";
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[j][k] = temp[k];
                    }
                }
                else if (Integer.parseInt(str[i][0]) == Integer.parseInt(str[j][0]) && Integer.parseInt(str[i][1]) > Integer.parseInt(str[j][1])) {
                    for (k = 0; k < 1000; ++k) {
                        temp[k] = str[i][k];
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[i][k] = "a";
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[i][k] = str[j][k];
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[j][k] = "a";
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[j][k] = temp[k];
                    }
                }
                else if (Integer.parseInt(str[i][0]) == Integer.parseInt(str[j][0]) && Integer.parseInt(str[i][1]) == Integer.parseInt(str[j][1]) && Integer.parseInt(str[i][2]) < Integer.parseInt(str[j][2])) {
                    for (k = 0; k < 1000; ++k) {
                        temp[k] = str[i][k];
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[i][k] = "a";
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[i][k] = str[j][k];
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[j][k] = "a";
                    }
                    for (k = 0; k < 1000; ++k) {
                        str[j][k] = temp[k];
                    }
                }
                else if (Integer.parseInt(str[i][0]) == Integer.parseInt(str[j][0]) && Integer.parseInt(str[i][1]) == Integer.parseInt(str[j][1]) && Integer.parseInt(str[i][2]) == Integer.parseInt(str[j][2])) {
                    for (k = 0; k < 1000 && str[i][k] != "a"; ++k) {}
                    final int i_index = k;
                    for (k = 0; k < 1000 && str[j][k] != "a"; ++k) {}
                    final int j_index = k;
                    if (i_index >= 4 && j_index >= 4 && Integer.parseInt(str[i][i_index - 2]) > Integer.parseInt(str[j][j_index - 2])) {
                        for (k = 0; k < 1000; ++k) {
                            temp[k] = str[i][k];
                        }
                        for (k = 0; k < 1000; ++k) {
                            str[i][k] = "a";
                        }
                        for (k = 0; k < 1000; ++k) {
                            str[i][k] = str[j][k];
                        }
                        for (k = 0; k < 1000; ++k) {
                            str[j][k] = "a";
                        }
                        for (k = 0; k < 1000; ++k) {
                            str[j][k] = temp[k];
                        }
                    }
                }
                for (int z = 0; z < 1000; ++z) {
                    temp[z] = "a";
                }
            }
        }
        try {
            final File file = new File(fileaddr);
            if (file.delete()) {
                System.out.println(String.valueOf(file.getName()) + " is deleted!");
            }
            else {
                System.out.println("Delete operation is failed.");
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
        try {
            final File file = new File(fileaddr);
            if (!file.exists()) {
                file.createNewFile();
            }
            final FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
            final BufferedWriter bw = new BufferedWriter(fw);
            for (int i = 0; i < p; ++i) {
                for (int j = 0; j < 1000; ++j) {
                    if (!str[i][j].equals("a")) {
                        bw.write(str[i][j]);
                        bw.write(" ");
                    }
                }
                bw.newLine();
            }
            bw.close();
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public void bring() {
        try {
            final BufferedReader br = new BufferedReader(new FileReader(new File("C:/Users/rahul singh/workspace/webcrawler/Asinfo.txt")));
            String[] splitted = null;
            final ArrayList<String> crawl = new ArrayList<String>();
            String strline;
            while ((strline = br.readLine()) != null) {
                splitted = strline.split(" ");
                final String as = splitted[0].substring(2);
                final String write = String.valueOf(as) + " " + splitted[2];
                crawl.add(write);
            }
            br.close();
            for (final String s : crawl) {
                System.out.println(s);
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public void pathinference(final String prefix, final String fprefix) {
        final Queue<String> q = new LinkedList<String>();
        for (final String s : this.base) {
            q.add(s);
        }
        while (q.size() > 0) {
            final String curras = q.remove();
            System.out.println(String.valueOf(prefix) + "TESTING(while) : CURRENT AS IS REMOVED FROM THE QUEUE");
            System.out.println(String.valueOf(prefix) + "TESTING(while) : SIZE OF THE QUEUE IS : " + q.size());
            final String peeraddress = String.valueOf(this.workingDir) + "/peers/" + curras + ".txt";
            try {
                final File file = new File(peeraddress);
                if (!file.exists()) {
                    this.extrapeer(curras);
                }
            }
            catch (Exception e) {
                e.printStackTrace();
                e.getCause();
            }
            try {
                final ArrayList<String> peers = new ArrayList<String>();
                peers.clear();
                final BufferedReader br = new BufferedReader(new FileReader(new File(peeraddress)));
                String strline;
                while ((strline = br.readLine()) != null) {
                    peers.add(strline);
                }
                System.out.println(String.valueOf(prefix) + "TESTING : ALL PEERS FROM THE PEER LIST ARE ADDED IN THE PEER ARRAYLIST");
                br.close();
                for (final String s2 : peers) {
                    System.out.println(String.valueOf(prefix) + "TESTING : peer(for) - NEW PEER FROM peers ARRAYLIST");
                    final String pathaddress = String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + curras + ".txt";
                    String line = null;
                    String[] spltd = null;
                    final ArrayList<String> newpath = new ArrayList<String>();
                    newpath.clear();
                    final BufferedReader br2 = new BufferedReader(new FileReader(new File(pathaddress)));
                    line = br2.readLine();
                    spltd = line.split(" ");
                    for (int i = 0; i < spltd.length; ++i) {
                        newpath.add(spltd[i]);
                    }
                    br2.close();
                    final BufferedReader cbr = new BufferedReader(new FileReader(new File(String.valueOf(this.workingDir) + "/caidarel.txt")));
                    String[] csplitted = null;
                    int flag = -1;
                    if (Integer.parseInt(newpath.get(0)) > 1) {
                        final String str1 = newpath.get(newpath.size() - 2);
                        final String str2 = newpath.get(newpath.size() - 1);
                        int rel = -1;
                        String cstrline;
                        while ((cstrline = cbr.readLine()) != null) {
                            csplitted = cstrline.split(" ");
                            if (csplitted[0].equals(str1) && csplitted[1].equals(str2) && csplitted[2].equals("-1")) {
                                rel = 1;
                                break;
                            }
                            if (csplitted[0].equals(str2) && csplitted[1].equals(str1) && csplitted[2].equals("-1")) {
                                rel = 0;
                                break;
                            }
                            if (csplitted[0].equals(str1) && csplitted[1].equals(str2) && csplitted[2].equals("0")) {
                                rel = 2;
                                break;
                            }
                            if (csplitted[0].equals(str2) && csplitted[1].equals(str1) && csplitted[2].equals("0")) {
                                rel = 2;
                                break;
                            }
                        }
                        cbr.close();
                        if (rel == 0) {
                            final BufferedReader checkbr = new BufferedReader(new FileReader(new File(String.valueOf(this.workingDir) + "/caidarel.txt")));
                            String checkstrline;
                            while ((checkstrline = checkbr.readLine()) != null) {
                                final String[] checksplitted = checkstrline.split(" ");
                                if (checksplitted[0].equals(newpath.get(newpath.size() - 1)) && checksplitted[1].equals(s2) && checksplitted[2].equals("-1")) {
                                    flag = 1;
                                    checkbr.close();
                                    break;
                                }
                                if (checksplitted[1].equals(newpath.get(newpath.size() - 1)) && checksplitted[0].equals(s2) && checksplitted[2].equals("-1")) {
                                    flag = 1;
                                    checkbr.close();
                                    break;
                                }
                                if (checksplitted[0].equals(newpath.get(newpath.size() - 1)) && checksplitted[1].equals(s2) && checksplitted[2].equals("0")) {
                                    flag = 1;
                                    checkbr.close();
                                    break;
                                }
                                if (checksplitted[1].equals(newpath.get(newpath.size() - 1)) && checksplitted[0].equals(s2) && checksplitted[2].equals("0")) {
                                    flag = 1;
                                    checkbr.close();
                                    break;
                                }
                            }
                        }
                        else if (rel == 1) {
                            final BufferedReader checkbr = new BufferedReader(new FileReader(new File(String.valueOf(this.workingDir) + "/caidarel.txt")));
                            String checkstrline;
                            while ((checkstrline = checkbr.readLine()) != null) {
                                final String[] checksplitted = checkstrline.split(" ");
                                if (checksplitted[0].equals(newpath.get(newpath.size() - 1)) && checksplitted[1].equals(s2) && checksplitted[2].equals("-1")) {
                                    flag = 1;
                                    checkbr.close();
                                    break;
                                }
                            }
                        }
                        else if (rel == 2) {
                            final BufferedReader checkbr = new BufferedReader(new FileReader(new File(String.valueOf(this.workingDir) + "/caidarel.txt")));
                            String checkstrline;
                            while ((checkstrline = checkbr.readLine()) != null) {
                                final String[] checksplitted = checkstrline.split(" ");
                                if (checksplitted[0].equals(newpath.get(newpath.size() - 1)) && checksplitted[1].equals(s2) && checksplitted[2].equals("-1")) {
                                    flag = 1;
                                    checkbr.close();
                                    break;
                                }
                            }
                        }
                    }
                    else {
                        String cstrline;
                        while ((cstrline = cbr.readLine()) != null) {
                            csplitted = cstrline.split(" ");
                            if (csplitted[0].equals(newpath.get(newpath.size() - 1)) && csplitted[1].equals(s2) && csplitted[2].equals("-1")) {
                                flag = 1;
                                cbr.close();
                                break;
                            }
                            if (csplitted[1].equals(newpath.get(newpath.size() - 1)) && csplitted[0].equals(s2) && csplitted[2].equals("-1")) {
                                flag = 1;
                                cbr.close();
                                break;
                            }
                            if (csplitted[0].equals(newpath.get(newpath.size() - 1)) && csplitted[1].equals(s2) && csplitted[2].equals("0")) {
                                flag = 1;
                                cbr.close();
                                break;
                            }
                            if (csplitted[1].equals(newpath.get(newpath.size() - 1)) && csplitted[0].equals(s2) && csplitted[2].equals("0")) {
                                flag = 1;
                                cbr.close();
                                break;
                            }
                        }
                    }
                    System.out.println(String.valueOf(prefix) + "TESTING(peer for) : CAIDA DATASET CHECKED");
                    if (flag == 1) {
                        System.out.println("PASS");
                    }
                    else {
                        System.out.println("FAIL");
                    }
                    final ArrayList<String> bestpath = new ArrayList<String>();
                    bestpath.clear();
                    final File file2 = new File(String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + s2 + ".txt");
                    if (file2.exists()) {
                        final String firstpath = String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + s2 + ".txt";
                        final BufferedReader br3 = new BufferedReader(new FileReader(new File(firstpath)));
                        final String line2 = br3.readLine();
                        String[] spltd2 = null;
                        spltd2 = line2.split(" ");
                        bestpath.clear();
                        for (int j = 0; j < spltd2.length; ++j) {
                            bestpath.add(spltd2[j]);
                        }
                        br3.close();
                    }
                    if (!this.base.contains(s2) && flag == 1 && !newpath.contains(s2)) {
                        newpath.add(s2);
                        final int x = Integer.parseInt(newpath.get(0)) + 1;
                        newpath.set(0, Integer.toString(x));
                        final int y = Integer.parseInt(newpath.get(1)) + 1;
                        newpath.set(1, Integer.toString(y));
                        System.out.println(String.valueOf(prefix) + "TESTING(peer for) : NEW PATH IS ADDED INTO THE TEXT FILE");
                        this.addnewpath(newpath, s2, fprefix);
                        final String faddr = String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + s2 + ".txt";
                        this.sortfile(faddr);
                        final int match = this.matchchecking(faddr, bestpath);
                        final String adr = String.valueOf(this.workingDir) + "/allASinfo/AS" + s2 + ".txt";
                        final BufferedReader br4 = new BufferedReader(new FileReader(new File(adr)));
                        final String orgline = br4.readLine();
                        final String[] arr = orgline.split(" ");
                        String type = "abc";
                        type = arr[1];
                        System.out.println(String.valueOf(prefix) + "TESTING(AS ORG CHECKING) : " + type);
                        br4.close();
                        if (match != 0 || q.contains(s2) || type.equalsIgnoreCase("ORG") || type.equalsIgnoreCase("ORIGIN") || this.base.contains(s2) || type.equals("abc")) {
                            continue;
                        }
                        q.add(s2);
                        System.out.println(String.valueOf(prefix) + "TESTING(queue addition) : " + q.size());
                    }
                }
            }
            catch (Exception e) {
                e.printStackTrace();
                e.getCause();
            }
        }
    }
    
    public int matchchecking(final String asfile, final ArrayList<String> path) {
        BufferedReader br = null;
        try {
            int count = 0;
            br = new BufferedReader(new FileReader(new File(asfile)));
            final String line = br.readLine();
            final String[] splitted = line.split(" ");
            if (splitted.length == path.size()) {
                for (int i = 3; i < splitted.length; ++i) {
                    if (splitted[i].equals(path.get(i))) {
                        ++count;
                    }
                }
            }
            if (count == splitted.length - 3 && count == path.size() - 3) {
                System.out.println("TESTING(match checking) : MATCHED");
                br.close();
                return 1;
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
        System.out.println("TESTING(match checking) : NOT MATCHED");
        try {
            br.close();
        }
        catch (IOException e2) {
            e2.printStackTrace();
        }
        return 0;
    }
    
    public void addnewpath(final ArrayList<String> newpath, final String s, final String fprefix) {
        int indi = -1;
        try {
            final File file = new File(String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + s + ".txt");
            if (!file.exists()) {
                file.createNewFile();
                indi = 1;
            }
            if (indi == 1) {
                final FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
                final BufferedWriter bw = new BufferedWriter(fw);
                for (int b = 0; b < newpath.size(); ++b) {
                    bw.write(newpath.get(b));
                    bw.write(" ");
                }
                bw.newLine();
                bw.close();
            }
            else {
                final BufferedReader br = new BufferedReader(new FileReader(new File(String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + s + ".txt")));
                String[] splitted = null;
                final File inFile = new File(String.valueOf(this.workingDir) + "/paths/" + fprefix + "/" + s + ".txt");
                if (!inFile.isFile()) {
                    System.out.println("Parameter is not an existing file");
                    return;
                }
                final File tempFile = new File(String.valueOf(inFile.getAbsolutePath()) + ".tmp");
                final PrintWriter pw = new PrintWriter(new FileWriter(tempFile));
                String strline;
                while ((strline = br.readLine()) != null) {
                    splitted = strline.split(" ");
                    final long x = Long.parseLong(splitted[splitted.length - 2]);
                    final long y = Long.parseLong(newpath.get(newpath.size() - 2));
                    if (x != y) {
                        pw.println(strline);
                        pw.flush();
                    }
                }
                for (int i = 0; i < newpath.size(); ++i) {
                    pw.print(newpath.get(i));
                    pw.print(" ");
                    pw.flush();
                }
                pw.println();
                pw.close();
                br.close();
                if (!inFile.delete()) {
                    System.out.println("Could not delete file");
                    return;
                }
                if (!tempFile.renameTo(inFile)) {
                    System.out.println("Could not rename file");
                }
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
    
    public void extrapeer(final String as) {
        System.out.println("EXTRA PEER FUNCTION");
        System.out.println("Current working directory : " + this.workingDir);
        final String fileaddress = String.valueOf(this.workingDir) + "/peers/";
        final ArrayList<String> peer = new ArrayList<String>();
        String[] splitted = null;
        try {
            final String fileaddr = String.valueOf(fileaddress.substring(0, fileaddress.length())) + as + ".txt";
            final File file = new File(fileaddr);
            if (!file.exists()) {
                file.createNewFile();
            }
            final FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
            final BufferedWriter bw = new BufferedWriter(fw);
            final BufferedReader br2 = new BufferedReader(new FileReader(new File(String.valueOf(this.workingDir) + "/SortFile_march.txt")));
            String strline;
            while ((strline = br2.readLine()) != null) {
                splitted = strline.split(" ");
                for (int i = 1; i < splitted.length; ++i) {
                    if (splitted[i].equals(as) && (i != splitted.length - 1 || i != 1)) {
                        if (i == splitted.length - 1) {
                            if (!peer.contains(splitted[i - 1])) {
                                peer.add(splitted[i - 1]);
                            }
                        }
                        else if (i == 1) {
                            if (!peer.contains(splitted[i + 1])) {
                                peer.add(splitted[i + 1]);
                            }
                        }
                        else {
                            if (!peer.contains(splitted[i - 1])) {
                                peer.add(splitted[i - 1]);
                            }
                            if (!peer.contains(splitted[i + 1])) {
                                peer.add(splitted[i + 1]);
                            }
                        }
                    }
                }
            }
            br2.close();
            for (final String s1 : peer) {
                if (!s1.equals(as)) {
                    bw.write(s1);
                    bw.newLine();
                }
            }
            bw.close();
            peer.clear();
            final String addr = String.valueOf(this.workingDir) + "/peers/";
            final String faddr = String.valueOf(addr) + as + ".txt";
            this.deleteblanklines(faddr);
        }
        catch (Exception e) {
            e.printStackTrace();
            e.getCause();
        }
    }
}